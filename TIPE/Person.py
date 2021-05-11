class Person:
    
    staticLastId = 0

    id = 0
    name = ""
    dob = ""
    hospital = ""
    medicalHistory = []
     
    def __init__(self, name, dob, hospital):
        self.id = staticLastId
        staticLastId += 1
        self.name = name
        self.dob = dob
        self.hospital = hospital
        self.medicalHistory = []






