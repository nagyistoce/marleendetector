from marleendetector.gallerymanager import *

class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return "<Person id:%s, name:%s>" % (self.id, self.name)

class FacesDBManager:
    """
        Manages the faces and person-face connections
    """
    def __init__(self):
        self.persons = self.__readPersonsFromFile()
        self.person_binding = {}
        pass
    

    def __readPersonsFromFile(self):
        #print GALLERY_PERSONS
        persons = []
        f = open(GALLERY_PERSONS, 'r')
        for index, line in enumerate(f):
            print index, line.strip()
            person = Person(index, line.strip())
            persons.append(person)

        return persons
     
    def bindPersonAndImage(self, person, image_id):
        if person in self.person_binding:
            # key exists, add value to array
            self.person_binding[image_id].append()
        
fdbManager = FacesDBManager()

#print man.readPersonsFromFile()