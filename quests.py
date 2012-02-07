
class QuestInfo:
    def __init__(self, moncounts={}, monlevels=(1,12),
                 itemcounts={}, dlevels=(1,12),
                 messages={}, gifts=None):
        self.moncounts = moncounts
        self.monlevels = monlevels
        self.itemcounts = itemcounts
        self.dlevels = dlevels
        self.messages = messages
        self.gifts = gifts

class QuestStock:
    def __init__(self):

        quest1 = QuestInfo(moncounts={3:1, 4:1, 5:2, 6:2, 7:3}, 
                           monlevels=(3,8),
                           itemcounts={3:1, 4:1, 5:1, 6:1, 7:1}, 
                           dlevels=(3,7),
                           messages={3: ['Victory! The Thunderdome grants you a gift!', 'An exit appears.'],
                                     4: ['Victory! The Thunderdome grants you a gift!', 'An exit appears.'],
                                     5: ['Victory! The Thunderdome grants you a gift!', 'An exit appears.'],
                                     6: ['Victory! The Thunderdome grants you a gift!', 'An exit appears.'],
                                     7: ['Total victory!', 'The Thunderdome grants you godlike powers!']}, 
                           gifts={3: [None, None, None],
                                  4: [None, None, None],
                                  5: [None, None, None],
                                  6: [None, None, None],
                                  7: ['deusex']})

        questkali = QuestInfo(moncounts={15:10},
                              monlevels=(8,11),
                              itemcounts={15:10},
                              dlevels=(15,15),
                              messages={15: []},
                              gifts={15: []})
        
        self.quests = {'q': quest1,
                       'qk': questkali}


    def get(self, branch):
        if branch in self.quests:
            return self.quests[branch]
        return None

