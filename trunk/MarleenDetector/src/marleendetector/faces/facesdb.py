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
        self.max_p_id = -1
        self.person_binding = {}
        self.persons = self.__readPersonsFromFile()
        pass
    
    def addPerson(self, personname):
        """
            personname the name of a person, string
        """
        next_id = self.max_p_id + 1
        self.max_p_id = next_id
        person = Person(next_id, personname.strip())
        self.persons.append(person)
        return person

    def __readPersonsFromFile(self):
        #print GALLERY_PERSONS
        persons = []
        f = open(GALLERY_PERSONS, 'r')
        for index, line in enumerate(f):
            print index, line.strip()
            person = Person(index, line.strip())
            persons.append(person)
            if self.max_p_id < index:
                self.max_p_id = index

        return persons
     
    def bindPersonAndImage(self, person, image_id):
        if person in self.person_binding:
            # key exists, add value to array
            self.person_binding[person].append(image_id)
        else:
            self.person_binding[person] = [image_id]
            
            
    def saveBindings(self):
        f = open(GALLERY_PERSON_BINDINGS, 'wr')
        for person in self.person_binding:
            f.write(person.name)
            f.write('\n')
            for img in self.person_binding[person]:
                f.write(img)
                f.write(' ')
            f.write('\n')
            print person
            print self.person_binding[person]
        f.close()


class FaceBindingsManager:
    def __init__(self):
        pass
    
    def readBindings(self, filename):
        bindings = {}
        f = open(filename, 'r')
        currentname = None
        for index, line in enumerate(f):
            if index % 2 == 0:
                # name line
                name = line.strip()
                currentname = name
            else:
                # normalized images of this person
                image_names = line.strip()
                bindings[currentname] = image_names.split()
        f.close()
        return bindings
    
if __name__ == "main":
    fdbManager = FacesDBManager()

#print man.readPersonsFromFile()