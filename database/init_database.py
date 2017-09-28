from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import *
from app import db as session
"""
   Load the database with malware...
"""

session.query(Item).delete()
session.query(Category).delete()
session.query(User).delete()

print("your old database has been wiped")
# malware_file  = open("database_items.txt", "r")
# malware = file.read()

malware = {"Virus" : "A virus is a type of malicious software\
            (malware) that when executed replicates\
            itself by modifying other programs and\
            inserts its own code.",
            "Rootkit": "A rootkit is a collection of computer software,\
             typically malicious, designed to enable access to a computer or\
             areas of its software that would not otherwise be allowed\
             (for example, to an unauthorized user) and often masks its\
             existence or the existence of other software.",
            "Worm":"A computer worm is a standalone malware computer\
             program that replicates itself in order to spread to other\
             computers",
            "Trojan":"In computing, Trojan horse, or Trojan,\
             is any malicious computer program which misleads\
             users of its true intent.",
            "Backdoor": "A backdoor is a method, often secret,\
             of bypassing normal authentication or encryption\
             in a computer system, a product, or an embedded device\
             (e.g. a home router), or its embodiment,\
             e.g. as part of a cryptosystem, an algorithm, or a chipset."}

virus = {"Melissa": "Named after an exotic dancer from Florida,\
         it was created by David L. Smith in 1999.\
         It started as an infected Word document that was posted up\
         on the alt.sex usenet group, claiming to be a list of passwords\
         for pornographic sites. This got people curious and when it was\
         downloaded and opened, it would trigger the macro inside\
         and unleash its payload.\
         The virus will mail itself to the top 50 people in the users\
         email address book and this caused an increase of email traffic,\
         disrupting the email services of governments and corporations.\
         It also sometimes corrupted documents by inserting a\
         Simpsons reference into them.",
         "iloveyou":"The ILOVEYOU virus is considered one of the most virulent\
          computer virus ever created and it is not hard to see why.\
          The virus managed to wreck havoc on computer systems\
          all over the world, causing damages totaling in at an estimate\
          of $10 billion. 10 percent of the worlds Internet-connected\
          computers were believed to have been infected.\
          It was so bad that governments and large corporations\
          took their mailing systems offline to prevent infection."}
worm = {"Code Red":
        "Code Red first surfaced on 2001 and was discovered by two eEye\
         Digital Security employees. It was named Code Red because the the pair\
         were drinking Code Red Mountain Dew at the time of discovery.\
         The worm targeted computers with Microsoft IIS web server installed,\
         exploiting a buffer overflow problem in the system.\
         It leaves very little trace on the hard disk as it is able\
         to run entirely on memory, with a size of 3,569 bytes.\
         Once infected, it will proceed to make a hundred copies\
         of itself but due to a bug in the programming,\
         it will duplicate even more and ends up eating\
         a lot of the systems resources.",
         "Sasser":"A Windows worm first discovered in 2004,\
          it was created by computer science student Sven Jaschan,\
          who also created the Netsky worm.\
          While the payload itself may be seen as simply annoying\
          (it slows down and crashes the computer,\
          while making it hard to reset without cutting the power),\
          the effects were incredibly disruptive,\
          with millions of computers being infected,\
          and important, critical infrastructure affected.\
          The worm took advantage of a buffer overflow vulnerability\
          in Local Security Authority Subsystem Service (LSASS),\
          which controls the security policy of local accounts\
          causing crashes to the computer. "}
trojan = {"Beast":
          "Beast is a Windows-based backdoor trojan horse,\
          more commonly known in the hacking community as a\
          Remote Administration Tool or a RAT.\
          It is capable of infecting versions of Windows from 95 to 10.\
          Written in Delphi and released first by its author Tataye in 2002.",
          "Njrat":
          "njRAT, also known as Bladabindi, is a Remote Access Tool or\
          Trojan which allows the holder of the program to control the end\
          users computer. It was first found in June 2013 with some\
          variants traced to November 2012. It was made by Arabic speaking\
          criminals and was often used against targets in the Middle East.\
          It can be spread through phishing and infected drives.\
          It is rated severe by the Microsoft Malware Protection Center.",
          "Zeus":
          "Zeus, ZeuS, or Zbot is a Trojan horse malware package that runs on\
           versions of Microsoft Windows. While it can be used to carry\
           out many malicious and criminal tasks, it is often used to steal\
           banking information by man-in-the-browser keystroke logging and form\
           grabbing. It is also used to install the CryptoLocker ransomware.\
           Zeus is spread mainly through drive-by\
           downloads and phishing schemes."}
backdoor = {"Back Orifice":
            "Back Orifice (often shortened to BO) is a computer program\
             designed for remote system administration.\
             It enables a user to control a computer\
             running the Microsoft Windows operating system\
             from a remote location.",
            "Win32.Hupigon":
            "Backdoor.Win32.Hupigon (also Backdoor.Win32.Graftor)\
             is a backdoor Trojan.Its first known detection goes back to\
             November, 2008, according to Securelist from Kaspersky Labs."}

session.add_all([
                 Category(name="Virus", description=malware.get("Virus")),
                 Category(name="Rootkit", description=malware.get("Rootkit")),
                 Category(name="Worm", description=malware.get("Worm")),
                 Category(name="Backdoor", description=malware.get("Backdoor")),
                 Category(name="Trojan", description=malware.get("Trojan"))
                 ])
session.commit()

# add items but first add users guest and admin.
# id, title, description, image, catagory_id, item_category, creator_id,
# creation_date

session.add_all([User(social_id=1,name="admin", email="sample@test.com"),
                 User(social_id=2,name="guest", email="guest@hotmail.com")])
session.commit()

indices = []
categories = session.query(Category);
for category in categories:
    indices.append(category.id)

# categories 1 = virus, 2 = rootkit, 3 is worm 4 = backdoor, 5 = trojan

session.add_all([
Item(title="iloveyou", description=virus.get("iloveyou"),category=indices[0], creator=1),
Item(title="Melissa", description=virus.get("Melissa"),category=indices[0], creator=1),
Item(title="Code Red", description=worm.get("Code Red"),category=indices[2], creator=1),
Item(title="Sasser", description=worm.get("Sasser"),category=indices[2], creator=1),
Item(title="Beast", description=trojan.get("Beast"),category=indices[3], creator=1),
Item(title="Njrat", description=trojan.get("Njrat"),category=indices[3], creator=2),
Item(title="Zeus", description=trojan.get("Zeus"),category=indices[3], creator=2),
Item(title="Back Orifice", description=backdoor.get("Back Orifice"),\
     category=indices[4], creator=2),
Item(title="Win32.Hupigon", description=backdoor.get("Win32.Hupigon"),\
     category=indices[4], creator=2)
])
session.commit()


print("Database (matrix) reloaded")
categories = session.query(Category).all()
print("Categories")
print("-------------")
for category in categories:
    print(category.name)
print("Users")
print("--------------")
users = session.query(User).all()
for user in users:
    print("name: " + user.name)
    print("email: " + user.email)

print("Items")
print("------------------")
items = session.query(Item).all()
for item in items:
    print("title: " + item.title)
    print("description " + item.description)
    print("id of category: " + str(item.category))
    category = session.query(Category).filter_by(id=item.category).one()
    print(category.name)
