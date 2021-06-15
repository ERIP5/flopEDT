# Imports des modules
from requests import Session # API HP
from requests.auth import HTTPBasicAuth # API HP
from zeep import Client # API HP
from zeep.transports import Transport # API HP
from math import gcd # PGCD
from functools import reduce # Pour le pgcd d'une liste
from tqdm import tqdm # Affichage de la barre sympa

from django.db import transaction
from base.models import CourseType, RoomType, StructuralGroup, Module, Course
from people.models import Tutor
from misc.assign_colors import assign_module_color


#Fonction osef
def inputBool(message=""): #y/n
    while True:
        ans = input("(Boolean) - "+message).lower()
        if ans in ["y","n","yes","no","o","non","oui","true","false","t","f"]:
            if ans in ["y","yes","o","oui","t","true"]: return True
            else: return False
        else:
            print("Retry ('y' or 'n' only)")


def inputInt(message=""):  #Un entier. Si c'est un float alors tronqué
    ans = ""
    while type(ans) != int:
        ans = input("(Integer) - "+message)
        try:
            ans = int(float(ans))
        except:
            print("Retry (int only, float will be floored)")
    return ans


def inputTime(message=""): #Au format HH:mm
    ans = ""
    while type(ans)!= int:
        inp = input("( HH:mm ) - "+message)
        try:
            heure, minute = inp.split(":")
            heure = int(heure)
            minute = int(minute)
            if 0<=heure<=24 and 0<=minute<=59:
                ans = heure*60+minute
            else:
                print("Retry ( 0<=hours<=24 and 0<=minutes<=59 )")
        except:
            print("Retry (use HH:mm format)")
    return ans


def cleanDictionary(dictionary): #Nettoie un dictionnaire des clés menant vers None
    keysToDelete = []
    for i in dictionary:
        if dictionary[i]==None:
            keysToDelete.append(i)
    for i in keysToDelete:
        dictionary.pop(i)


def getpSvcWDureeToMinutesInDay(pSvcWDuree): #Pour convertir le temps Hyperplanning en minute dans une journee (peu import quelle journée) et la journée
    timeInMinutes = pSvcWDuree*24*60
    listDays = ['m','tu','w','th','f','sa','su']
    return (round(timeInMinutes%(60*24)),listDays[round(pSvcWDuree)])


def PGCDListe(liste):   #Utilisé pour calculer la 'granularite'
    return reduce(gcd,liste)
    
#Fonctions secondaires
def creerPeriodes():
    dictionnairePeriodes = dict()
    nombreDePeriodes = inputInt("Nombre de periodes (semestre, trimestre, ...): ")
    for i in range(nombreDePeriodes):
        nomDePeriode = input("Periode "+str(1+i)+"/"+str(nombreDePeriodes)+". Donnez un nom à cette période: ")
        semaineDebutPeriode = inputInt("Semaine de début de la période "+nomDePeriode+": ")
        semaineFinPeriode = inputInt("Semaine de fin de la période "+nomDePeriode+": ")
        dictionnairePeriodes[nomDePeriode] = (semaineDebutPeriode,semaineFinPeriode)
    print("")
    return dictionnairePeriodes


def creerJoursSemaine():
    joursSemaines = ['m','tu','w','th','f','sa','su']
    nomJours = ['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']
    ans = []
    for i in range(7):
        coursCeJour = inputBool("Cours le "+nomJours[i]+" ? (y/n) ")
        if coursCeJour:
            ans.append(joursSemaines[i])
    return ans


def creerPauseMeridienne():
    print("(Astuce ) - Mettre 13:00 pour le debut et la fin si vous changez d'avis et ne souhaitez pas de pause")
    debutPause = inputTime("À quelle heure la pause commencera? ")
    finPause = inputTime("À quelle heure la pause se finira? ")
    while debutPause>finPause:
        print("(!!!!!!!) - La pause se fini avant de commencer! Ça n'a pas de sens")
        debutPause = inputTime("À quelle heure la pause commencera? ")
        finPause = inputTime("À quelle heure la pause se finira? ")    
    return debutPause, finPause


def getValidCourseKeys(IHpSvcWCours,breakLevel=-1): # Certainement possible d'accelerer tout ça, mais les fonctions de l'API ne fonctionnent pas...
    listCoursesKeys = IHpSvcWCours.service.TousLesCours()#[0:breakLevel]
    if len(listCoursesKeys)>breakLevel:
        listCoursesKeys = listCoursesKeys[0:breakLevel]

    
    validCourseKeys = []
    for i in tqdm(listCoursesKeys,"Courses - Validating : ", bar_format='{l_bar}{bar:15}{r_bar}{bar:-10b}'):
        if IHpSvcWCours.service.CoursEstUnCoursFils(i) or IHpSvcWCours.service.CoursEstUnCoursSimple(i):
            if not IHpSvcWCours.service.EstCoursNonPlace(i):
                validCourseKeys.append(i)
    return validCourseKeys


def extractRooms(IHpSvcWSalles): #Fini :)
    listRoomKeys = IHpSvcWSalles.service.ToutesLesSalles()
    listRoomNames = []
    for i in tqdm(listRoomKeys,"Room    - Extracting : ", bar_format='{l_bar}{bar:15}{r_bar}{bar:-10b}'):
        listRoomNames.append(IHpSvcWSalles.service.NomSalle(i))
    return set(listRoomNames)


def extractPeople(IHpSvcWEnseignants): #Fini
    listTeachersKeys = IHpSvcWEnseignants.service.TousLesEnseignants()
    teacherDictionary = {}
    for i in tqdm(listTeachersKeys,"Teacher - Extracting : ", bar_format='{l_bar}{bar:15}{r_bar}{bar:-10b}'):
        teacherSubDictionary = {}
        teacherSubDictionary["first_name"] = IHpSvcWEnseignants.service.PrenomEnseignant(i)
        teacherSubDictionary["last_name"] = IHpSvcWEnseignants.service.NomEnseignant(i)
        email = IHpSvcWEnseignants.service.EMailEnseignant(i)
        if email is None:
            teacherSubDictionary["email"] = 'fake@flopedt.org'
        else:
            teacherSubDictionary["email"] = email
        teacherSubDictionary["status"] = "temp" # Pas necessaire
        teacherSubDictionary["employer"] = "temp" # Pas necessaire
        teacherID = IHpSvcWEnseignants.service.IdentifiantCASEnseignant(i)
        if teacherID != None:   #A modifier
            teacherDictionary[teacherID] = teacherSubDictionary
    return teacherDictionary


def extractModules(IHpSvcWMatieres,IHpSvcWCours,IHpSvcWTDOption,IHpSvcWPromotions,validCourseKeys,firstPeriod): #Devrait bien avoir un moyen plus simple de faire ça...
    listCoursesKeys = validCourseKeys    
    tempDictNameOfModules = {} #Cle -> Nom
    moduleDictionary = {}
    for i in tqdm(listCoursesKeys,"Modules - Extracting : ", bar_format='{l_bar}{bar:15}{r_bar}{bar:-10b}'):
        moduleKey = IHpSvcWCours.service.MatiereCours(i)
        if moduleKey not in tempDictNameOfModules.keys():
            moduleName = IHpSvcWMatieres.service.LibelleMatiere(moduleKey)
            tempDictNameOfModules[moduleKey] = moduleName
        else:
            moduleName = tempDictNameOfModules[moduleKey]
            
        courseTDOpt = IHpSvcWCours.service.TDOptionsDuCours(i)
        courseProm = IHpSvcWCours.service.PromotionsDuCours(i)
        courseOwner = IHpSvcWMatieres.service.ProprietaireMatiere(IHpSvcWCours.service.MatiereCours(i))
        
        for j in courseTDOpt: 
            promOfTDOpt = IHpSvcWTDOption.service.PromotionTDOption(j)
            if promOfTDOpt not in courseProm:
                courseProm.append(promOfTDOpt)
        for j in courseProm:
            promName = IHpSvcWPromotions.service.NomPromotion(j)
            if moduleName in moduleDictionary.keys():
                if moduleDictionary[moduleName] == None:
                    advancedModuleName = moduleName+"_"+promName
                    moduleDictionary[advancedModuleName] = {'short':moduleName,'PPN':'Code PPN','name':moduleName,'promotion':promName,'period':firstPeriod,'responsable':courseOwner}
                elif moduleDictionary[moduleName]['promotion'] != promName:
                    advancedModuleName = moduleName+"_"+promName
                    moduleDictionary[advancedModuleName] = {'short':moduleName,'PPN':'Code PPN','name':moduleName,'promotion':promName,'period':firstPeriod,'responsable':courseOwner}
                    advancedOldModuleName = moduleName+"_"+moduleDictionary[moduleName]["promotion"]
                    moduleDictionary[advancedOldModuleName] = moduleDictionary.pop(moduleName)
                    moduleDictionary[moduleName] = None
            else:
                moduleDictionary[moduleName] = {'short':moduleName,'PPN':'Code PPN','name':moduleName,'promotion':promName,'period':firstPeriod,'responsable':courseOwner}
    cleanDictionary(moduleDictionary)
    return moduleDictionary


def extractCoursesSettings(IHpSvcWCours,validCourseKeys): #Fini
    coursesSettingsDictionary = {}
    for i in tqdm(validCourseKeys,"Courses - Extracting : ", bar_format='{l_bar}{bar:15}{r_bar}{bar:-10b}'):    #for i in validCourseKeys:
        courseType = IHpSvcWCours.service.TypeCours(i)
        courseLength = getpSvcWDureeToMinutesInDay(IHpSvcWCours.service.DureeCours(i))[0]
        courseStartTime, courseDay = getpSvcWDureeToMinutesInDay(IHpSvcWCours.service.PlaceCours(i))
        courseKey = courseType+"_"+str(courseLength)+"m"
        if courseKey not in coursesSettingsDictionary.keys():
            coursesSettingsDictionary[courseKey] = {'duration':courseLength,'group_types':set(),'start_times':set()}
            coursesSettingsDictionary[courseKey]['group_types'].add(courseType)
        if courseStartTime not in coursesSettingsDictionary[courseKey]['start_times']:
            coursesSettingsDictionary[courseKey]['start_times'].add(courseStartTime)
    return coursesSettingsDictionary


def extractSettings(IHpSvcWCours,validCourseKeys): #Fini
    settingsDictionary = {"lunch_break_start_time":12*60,"lunch_break_finish_time":14*60}
    startTimes = set()
    finishTimes = set()
    days = set()
    for i in tqdm(validCourseKeys,"Setting - Extracting : ", bar_format='{l_bar}{bar:15}{r_bar}{bar:-10b}'): #for i in validCourseKeys:
        courseLength = getpSvcWDureeToMinutesInDay(IHpSvcWCours.service.DureeCours(i))[0]
        courseStartTime, courseDay = getpSvcWDureeToMinutesInDay(IHpSvcWCours.service.PlaceCours(i))
        courseFinishTime = courseStartTime+courseLength
        startTimes.add(courseStartTime)
        finishTimes.add(courseFinishTime)
        days.add(courseDay)
        
    settingsDictionary['day_start_time'] = min(startTimes)
    settingsDictionary['day_finish_time'] = max(finishTimes)
    settingsDictionary['days'] = list(days)
    settingsDictionary['default_preference_duration'] = PGCDListe(list(startTimes))
    return settingsDictionary


def extractPromotions(IHpSvcWPromotions): #Fini
    promKeys = IHpSvcWPromotions.service.ToutesLesPromotions()
    promotionDictionary = {}
    for i in tqdm(promKeys,"Proms   - Extracting : ", bar_format='{l_bar}{bar:15}{r_bar}{bar:-10b}'): 
        promName = IHpSvcWPromotions.service.NomPromotion(i)
        promotionDictionary[promName]=promName
    return promotionDictionary


def extractGroupTypes(coursesSettingsDict): #Fini
    groupTypesDict = set()
    for i in tqdm(coursesSettingsDict,"Types   - Extracting : ", bar_format='{l_bar}{bar:15}{r_bar}{bar:-10b}'):
        for j in coursesSettingsDict[i]['group_types']:
            groupTypesDict.add(j)
    return groupTypesDict


def extractGroups(IHpSvcWPromotions,IHpSvcWTDOptions): #Fini mais pas satisfait!
    groupDictionary = {}
    tdOptionsKeys = IHpSvcWTDOptions.service.TousLesTDOptions()
    promKeys = IHpSvcWPromotions.service.ToutesLesPromotions()

    for i in tqdm(promKeys,"Groups1 - Extracting : ", bar_format='{l_bar}{bar:15}{r_bar}{bar:-10b}'):
        promName = IHpSvcWPromotions.service.NomPromotion(i)
        groupID = (promName,promName)
        groupDictionary[groupID] = {"group_type":None,"parent":set()}
    
    for i in tqdm(tdOptionsKeys,"Groups2 - Extracting : ", bar_format='{l_bar}{bar:15}{r_bar}{bar:-10b}'):
        tdOptionName = IHpSvcWTDOptions.service.NomTDOption(i)
        belongTo = set()
        belongTo.add(IHpSvcWPromotions.service.NomPromotion(IHpSvcWTDOptions.service.PromotionTDOption(i)))
        groupID = (tdOptionName,IHpSvcWPromotions.service.NomPromotion(IHpSvcWTDOptions.service.PromotionTDOption(i)))  #A modifier

        groupDictionary[groupID] = {"group_type":None,"parent":belongTo}

    return groupDictionary


#Fonctions primaires
def demanderModifEventuelles(dico):
    print(" ") #Pour que ce soit plus propre
    if inputBool("Souhaitez-vous passez en revue certaines informations extraites et les modifier si besoin? : "):
        if inputBool("Les cours commenceront au plus tôt à: "+str(dico['settings']['day_start_time']//60)+"H"+str(dico['settings']['day_start_time']%60)+". Modifier? "):
            dico['settings']['day_start_time'] = inputTime("À quelle heure les cours doivent commencer? : ")
            
        if inputBool("Les cours se finiront au plus tard à: "+str(dico['settings']['day_finish_time']//60)+"H"+str(dico['settings']['day_finish_time']%60)+". Modifier? "):
            dico['settings']['day_finish_time'] = inputTime("À quelle heure les cours doivent finir? : ")
            
        if inputBool("Il n'y a actuellement pas de pause le midi. En définir une? : "):
            debutPauseMidi, finPauseMidi = creerPauseMeridienne()
            dico['settings']['lunch_break_start_time'] = debutPauseMidi
            dico['settings']['lunch_break_finish_time'] = finPauseMidi
            
        if inputBool("La distance minimale entre 2 cours sera de "+str(dico['settings']['default_preference_duration'])+" minutes. Modifier? : "):
            dico['settings']['default_preference_duration'] = inputInt("Quelle est la précision de plaçage de cours? (en minutes) : ")

        # Modifier
        messageJours = "Les jours de cours sont actuellement:"
        dicoJours = {"m":"Lundi","tu":"Mardi","w":"Mercredi","th":"Jeudi","f":"Vendredi","sa":"Samedi","su":"Dimanche"}
        for i in ["m","tu","w","th","f","sa","su"]:            
            if i in dico["settings"]["days"]: messageJours = messageJours + " "+dicoJours[i]
        messageJours = messageJours+". Modifier? : "
            
        if inputBool(messageJours):
            dico['settings']['days'] = creerJoursSemaine()

        return dico    
    else:
        return dico


#Fonction principale
def filldico(username,password,lPrefixeWsdl):
    # Initialisation et connexion
    session = Session()
    session.auth = HTTPBasicAuth(username,password)

    # Creation du dictionnaire
    rooms= set()
    room_groups= dict()
    room_categories= dict()
    people= dict()
    modules= dict()
    courses= dict()
    settings= dict()
    promotions= dict()
    group_types= set()
    groups= dict()    

    # Creation des services
    adminService = Client(lPrefixeWsdl + 'IHpSvcWAdmin', transport=Transport(session=session))
    roomService = Client(lPrefixeWsdl + 'IHpSvcWSalles', transport=Transport(session=session))    
    peopleService = Client(lPrefixeWsdl + 'IHpSvcWEnseignants', transport=Transport(session=session))
    moduleService = Client(lPrefixeWsdl + 'IHpSvcWMatieres', transport=Transport(session=session))
    courseService = Client(lPrefixeWsdl + 'IHpSvcWCours',transport=Transport(session=session))
    tdOptionService = Client(lPrefixeWsdl + 'IHpSvcWTDOptions',transport=Transport(session=session))
    promService = Client(lPrefixeWsdl + 'IHpSvcWPromotions',transport=Transport(session=session))
    

    # Verification des identifiants
    try:
        print ('Connected to: ' + adminService.service.Version()+"\n")
    except:
        print('Connection failed: either your username/password combination is wrong or your connection is down. Maybe both')
        return None

    # Creation periodes
    periodes = creerPeriodes()
    
    # Tout le tralala
    NOMBRE_DE_COURS_MAX = -1 # Utiliser pour accelerer les test. -1 si pas de limites.
    
    validCoursesKeys = getValidCourseKeys(courseService,NOMBRE_DE_COURS_MAX)
    
    rooms = extractRooms(roomService)
    room_groups = {}
    room_categories = {'all':rooms.copy()}

    people = extractPeople(peopleService)
    
    modules = extractModules(moduleService,courseService,tdOptionService,promService,validCoursesKeys,list(periodes.keys())[0]) #Pas beau
    
    courses = extractCoursesSettings(courseService, validCoursesKeys)

    settings = extractSettings(courseService,validCoursesKeys)
    settings['periods'] = periodes

    promotions = extractPromotions(promService)

    group_types = extractGroupTypes(courses)
    
    groups = extractGroups(promService,tdOptionService)

    #Demander si certains changement dans le dico (pause meridienne, heure debut et fin, jours 'ouvrable' et granularitee)
    book = {'rooms' : rooms,
            'room_groups' : room_groups,
            'room_categories' : room_categories,
            'people' : people,
            'modules' : modules,
            'courses' : courses,
            'settings' : settings,
            'promotions': promotions,
            'group_types' : group_types,
            'groups' : groups }
    
    book = demanderModifEventuelles(book)
    
    return book


def create_course_list_from_hp(username, password, lPrefixeWsdl,
                               remove_courses_with_no_group=True):
    # Initialisation et connexion
    session = Session()
    session.auth = HTTPBasicAuth(username, password)

    adminService = Client(lPrefixeWsdl + 'IHpSvcWAdmin', transport=Transport(session=session))
    courseService = Client(lPrefixeWsdl + 'IHpSvcWCours', transport=Transport(session=session))
    peopleService = Client(lPrefixeWsdl + 'IHpSvcWEnseignants', transport=Transport(session=session))
    promService = Client(lPrefixeWsdl + 'IHpSvcWPromotions', transport=Transport(session=session))
    tdOptService = Client(lPrefixeWsdl + 'IHpSvcWTDOptions', transport=Transport(session=session))
    moduleService = Client(lPrefixeWsdl + 'IHpSvcWMatieres', transport=Transport(session=session))

    # Verification des identifiants
    try:
        print('Connected to: ' + adminService.service.Version() + "\n")
    except:
        print(
            'Connection failed: either your username/password combination is wrong or your connection is down. Maybe both')
        return None

    validCourseKeys = getValidCourseKeys(courseService, 5000)

    coursesList = []

    for i in tqdm(validCourseKeys, "Courses - Extracting : ", bar_format='{l_bar}{bar:15}{r_bar}{bar:-10b}'):
        # type
        courseType = courseService.service.TypeCours(i) + "_" + str(
            round(courseService.service.DureeCours(i) * 24 * 60)) + "m"

        # room_type
        roomType = 'all'  # Temporaire

        # number
        courseNumber = 0

        # tutor and supp_tutor
        listOfTutors = courseService.service.EnseignantsDuCours(i)
        courseTutor = None
        courseSuppTutor = set()
        if len(listOfTutors) == 1:
            courseTutor = peopleService.service.IdentifiantCASEnseignant(listOfTutors[0])
        elif len(listOfTutors) > 1:
            for j in listOfTutors:
                courseSuppTutor.add(peopleService.service.IdentifiantCASEnseignant(j))

        # groups
        listOfCourseProms = courseService.service.PromotionsDuCours(i)
        listOfCourseTDOpt = courseService.service.TDOptionsDuCours(i)
        courseGroups = set()
        for j in listOfCourseProms:
            courseGroups.add(promService.service.NomPromotion(j))
        for j in listOfCourseTDOpt:
            courseGroups.add(tdOptService.service.NomTDOption(j))

        # module
        courseModule = moduleService.service.LibelleMatiere(courseService.service.MatiereCours(i))

        # week and year
        courseWeek = None
        hpWeek = courseService.service.DomaineCours(i)
        if len(hpWeek) > 0:
            hpWeek = hpWeek[0]
            courseWeek = courseService.service.SemaineEnSemaineCalendaire(hpWeek)
            courseYear = str(courseService.service.SemaineEnDate(hpWeek))[0:4]

        course = {"type": courseType,
                  "room_type": roomType,
                  "no": courseNumber,
                  "tutor": courseTutor,
                  "supp_tutor": courseSuppTutor,
                  "groups": courseGroups,
                  "module": courseModule,
                  "week": courseWeek,
                  "year": courseYear}

        if courseWeek != None:  # Modifier
            coursesList.append(course)

    if remove_courses_with_no_group:
        coursesList = remove_courses_without_group(coursesList)

    return coursesList


def remove_courses_without_group(listOfCourses):
    numberOfCourses = len(listOfCourses)
    for i in range(numberOfCourses - 1, -1, -1):
        if listOfCourses[i]['groups'] == set():
            listOfCourses.pop(i)
    return listOfCourses


@transaction.atomic
def extract_courses_from_book(courses_book, department, assign_colors=True):
    for c in courses_book:
        if not c['groups']:
            continue
        groups = StructuralGroup.objects.filter(name__in=c['groups'], train_prog__department=department)
        ct = CourseType.objects.get(name=c['type'], department=department)
        rt = RoomType.objects.get(name=c['room_type'], department=department)
        if c['tutor']:
            tut = Tutor.objects.get(username=c['tutor'])
        else:
            tut = None
        supp_tuts = Tutor.objects.filter(username__in = c['supp_tutor'])
        mod = Module.objects.get(name = c['module'], train_prog=groups[0].train_prog)
        new_course = Course(type=ct, room_type=rt, tutor=tut, module=mod, week=c['week'], year=c['year'])
        new_course.save()
        for g in groups:
            new_course.groups.add(g)
        for t in supp_tuts:
            new_course.supp_tutor.add(t)
    if assign_colors:
        assign_module_color(department)
    print("Course extraction done")