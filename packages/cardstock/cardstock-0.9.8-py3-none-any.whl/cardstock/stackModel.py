#!/usr/bin/python

import wx
from uiView import ViewModel, ViewProxy
from uiCard import CardModel
import version
from codeRunnerThread import RunOnMainSync

class StackModel(ViewModel):
    """
    This is the model for the stack.  It mostly just contains the cards as its children.
    """

    minSize = wx.Size(200, 200)

    def __init__(self, stackManager):
        super().__init__(stackManager)
        self.type = "stack"
        self.proxyClass = Stack

        self.properties["size"] = wx.Size(500, 500)
        self.properties["name"] = "stack"
        self.properties["canSave"] = False
        self.properties["canResize"] = False

        self.propertyTypes["canSave"] = 'bool'
        self.propertyTypes["canResize"] = 'bool'

        self.propertyKeys = []

        self.handlers = {}

    def AppendCardModel(self, cardModel):
        cardModel.parent = self
        self.childModels.append(cardModel)

    def InsertCardModel(self, index, cardModel):
        cardModel.parent = self
        self.childModels.insert(index, cardModel)

    def InsertNewCard(self, name, atIndex):
        card = CardModel(self.stackManager)
        card.SetProperty("name", self.DeduplicateName(name, [m.GetProperty("name") for m in self.childModels]))
        if atIndex == -1:
            self.AppendCardModel(card)
        else:
            self.InsertCardModel(atIndex, card)
            newIndex = self.childModels.index(self.stackManager.uiCard.model)
            self.stackManager.cardIndex = newIndex
        return card

    def RemoveCardModel(self, cardModel):
        cardModel.parent = None
        self.childModels.remove(cardModel)

    def GetCardModel(self, i):
        return self.childModels[i]

    def GetModelFromPath(self, path):
        parts = path.split('.')
        m = self
        for p in parts:
            found = False
            for c in m.childModels:
                if c.properties['name'] == p:
                    m = c
                    found = True
                    break
            if not found:
                return None
        return m

    def GetData(self):
        data = super().GetData()
        data["cards"] = [m.GetData() for m in self.childModels]
        data["properties"].pop("position")
        data["properties"].pop("name")
        data["CardStock_stack_format"] = version.FILE_FORMAT_VERSION
        data["CardStock_stack_version"] = version.VERSION
        return data

    def SetData(self, stackData):
        formatVer = stackData["CardStock_stack_format"]
        if formatVer != version.FILE_FORMAT_VERSION:
            self.MigrateDataFromFormatVersion(formatVer, stackData)

        super().SetData(stackData)
        self.childModels = []
        for data in stackData["cards"]:
            m = CardModel(self.stackManager)
            m.parent = self
            m.SetData(data)
            self.AppendCardModel(m)

        if formatVer != version.FILE_FORMAT_VERSION:
            self.MigrateModelFromFormatVersion(formatVer, self)

    def MigrateDataFromFormatVersion(self, fromVer, dataDict):
        if fromVer <= 2:
            """
            In File Format Version 3, some properties and methods were renamed.
            """
            # Update names
            def replaceNames(dataDict):
                if dataDict['type'] == "poly":
                    dataDict['type'] = "polygon"
                if "bgColor" in dataDict['properties']:
                    dataDict['properties']["fillColor"] = dataDict['properties'].pop("bgColor")
                if "border" in dataDict['properties']:
                    dataDict['properties']["hasBorder"] = dataDict['properties'].pop("border")
                if "editable" in dataDict['properties']:
                    dataDict['properties']["isEditable"] = dataDict['properties'].pop("editable")
                if "multiline" in dataDict['properties']:
                    dataDict['properties']["isMultiline"] = dataDict['properties'].pop("multiline")
                if "autoShrink" in dataDict['properties']:
                    dataDict['properties']["canAutoShrink"] = dataDict['properties'].pop("autoShrink")
                if 'childModels' in dataDict:
                    for child in dataDict['childModels']:
                        replaceNames(child)
            for c in dataDict['cards']:
                replaceNames(c)

    def MigrateModelFromFormatVersion(self, fromVer, stackModel):
        if fromVer <= 1:
            """
            In File Format Version 1, the cards used the top-left corner as the origin, y increased while moving down.
            In File Format Version 2, the cards use the bottom-left corner as the origin, y increases while moving up.
            Migrate all of the static objects to look the same in the new world order, but user code will need updating.
            Also update names of the old StopAnimations() and StopAllAnimations() methods, and move OnIdle to OnPeriodic.
            """
            def UnflipImages(obj):
                if obj.type == "image":
                    obj.PerformFlips(False, True)
                else:
                    for c in obj.childModels:
                        UnflipImages(c)

            for card in stackModel.childModels:
                card.PerformFlips(False, True)
                UnflipImages(card)

            # Update names of StopAnimating methods, OnIdle->OnPeriodic
            def replaceNames(obj):
                if "OnIdle" in obj.handlers:
                    obj.handlers["OnPeriodic"] = obj.handlers.pop("OnIdle")
                for k,v in obj.handlers.items():
                    val = v
                    val = val.replace(".StopAnimations(", ".StopAnimating(")
                    val = val.replace(".StopAllAnimations(", ".StopAllAnimating(")
                    obj.handlers[k] = val
                for child in obj.childModels:
                    replaceNames(child)
            replaceNames(stackModel)
        if fromVer <= 2:
            """
            In File Format Version 3, some properties and methods were renamed.
            """
            # Update names
            def replaceNames(obj):
                for k,v in obj.handlers.items():
                    if len(v):
                        val = v
                        val = val.replace(".bgColor", ".fillColor")
                        val = val.replace(".AnimateBgColor(", ".AnimateFillColor(")
                        val = val.replace(".border", ".hasBorder")
                        val = val.replace(".editable", ".isEditable")
                        val = val.replace(".multiline", ".isMultiline")
                        val = val.replace(".autoShrink", ".canAutoShrink")
                        val = val.replace(".visible", ".isVisible")
                        val = val.replace(".GetEventHandler(", ".GetEventCode(")
                        val = val.replace(".SetEventHandler(", ".SetEventCode(")
                        obj.handlers[k] = val
                for child in obj.childModels:
                    replaceNames(child)
            replaceNames(stackModel)


class Stack(ViewProxy):
    @property
    def numCards(self):
        return len(self._model.childModels)

    @property
    def currentCard(self):
        if self._model.didSetDown: return None
        return self._model.stackManager.uiCard.model.GetProxy()

    def CardWithNumber(self, number):
        model = self._model
        if model.didSetDown: return None
        if not isinstance(number, int):
            raise TypeError("CardWithNumber(): number is not an int")
        if number < 1 or number > len(model.childModels):
            raise ValueError("CardWithNumber(): number is out of bounds")
        return model.childModels[number-1].GetProxy()

    def Return(self, result=None):
        self._model.stackManager.runner.ReturnFromStack(result)

    def GetSetupValue(self):
        return self._model.stackManager.runner.GetStackSetupValue()

    def AddCard(self, name="card", atNumber=0):
        if not isinstance(name, str):
            raise TypeError("AddCard(): name is not a string")
        atNumber = int(atNumber)
        if atNumber < 0 or atNumber > len(self._model.childModels)+1:
            raise ValueError("AddCard(): atNumber is out of bounds")

        @RunOnMainSync
        def func():
            if self._model.didSetDown: return None
            return self._model.InsertNewCard(name, atNumber-1).GetProxy()
        return func()
