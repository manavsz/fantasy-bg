from my11circle import My11Circle 

    

class DataHandler:
    
    # self.fantasy = db.getDb('fantasy.json')
    # self.mc = My11Circle()

    def __init__(self, table):
        self.mc = My11Circle()
        self.fantasy = table


    def updateMatches(self):
        print('updating matches')
        matches = self.mc.getMatches()
        if 'matches' not in matches:
            self.mc.refreshSession()
            return self.updateMatches()
        
        data = matches['matches']

        for match in data['2']:

            if match['seriesId'] == 2391:

                players = self.mc.getMatchPoints(match['matchId'])

                match_db = {
                    'matchId': int(match['matchId']),
                    'seriesId': int(match['seriesId']),
                    'competition': match['competition'],
                    'displayName': match['displayName'],
                    'matchStartTime': match['matchStartTime'],
                    'players': players['players'],
                    'name': match['name'],
                    'matchStatus': match['matchStatus']

                }

                db_match = list(self.fantasy.find({'matchId': match['matchId']}))

                if len(db_match) == 0:
                    self.fantasy.insert_one(match_db)
                else:
                    self.fantasy.update_one({'matchId': match['matchId']}, {'$set': {'players': match_db['players']}})

        
        for match in data['3']:

            if match['seriesId'] == 2391:

                db_match = list(self.fantasy.find({'matchId': match['matchId']}))

                if len(db_match) == 0:
                    players = self.mc.getMatchPoints(match['matchId'])

                    match_db = {
                    'matchId': int(match['matchId']),
                    'seriesId': int(match['seriesId']),
                    'competition': match['competition'],
                    'displayName': match['displayName'],
                    'matchStartTime': match['matchStartTime'],
                    'players': players['players'],
                    'name': match['name'],
                    'matchStatus': match['matchStatus']
                    }
                    self.fantasy.insert_one(match_db)
                
                elif db_match[0]['matchStatus'] != 3:
                    players = self.mc.getMatchPoints(match['matchId'])

                    match_db = {
                    'matchId': int(match['matchId']),
                    'seriesId': int(match['seriesId']),
                    'competition': match['competition'],
                    'displayName': match['displayName'],
                    'matchStartTime': match['matchStartTime'],
                    'players': players['players'],
                    'name': match['name'],
                    'matchStatus': match['matchStatus']
                    }
                    self.fantasy.update_one({'matchId': match['matchId']}, {'$set': {'matchStatus': match_db['matchStatus'], 'players': match_db['players']}})


        return True