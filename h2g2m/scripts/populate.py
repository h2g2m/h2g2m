# -*- coding: utf-8 -*-
from h2g2m.models.tables import Root
import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from ..models import (
    Base,
    DBSession,
    Usr,
    Grp,
    Txt,
    Annotation,
    Post,
    TexHeader,
    Person
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        # Add a User
        adm_grp = Grp(name='hitchhiker')
        DBSession.add(adm_grp)
        DBSession.flush()
        adm_usr = Usr(login='hitchhiker', nickname='hitchhiker', language='English', passwd='tester', grp_id=adm_grp.id)
        # print get_state(adm_usr)
        DBSession.add(adm_usr)
        #print get_state(adm_usr)
        #adm_usr.language='Deutsch'
        #print get_state(adm_usr)
        DBSession.flush()
        #adm_usr.nickname='hitch'
        #DBSession.flush()

        atb = Grp(name='Algebra Team Bonn')
        rcm = Grp(name='Reading Class Mumford')
        hcm = Grp(name='Hausdorff Center')
        lars = Grp(name='Lars')
        jesko = Grp(name='Jesko')
        nikolai = Grp(name='Nikolai')
        hanno = Grp(name='Hanno')
        ulrike = Grp(name='Ulrike')
        admins = Grp(name='Admins')
        moderators = Grp(name='Moderators')
        tagger = Grp(name='Tag-Assistants')
        frehse = Grp(name='Frehse')
        bob = Grp(name='Bob')
        alice = Grp(name='Alice')

        DBSession.add(atb)
        DBSession.add(rcm)
        DBSession.add(hcm)
        DBSession.add(lars)
        DBSession.add(jesko)
        DBSession.add(nikolai)
        DBSession.add(hanno)
        DBSession.add(frehse)
        DBSession.add(ulrike)
        DBSession.add(admins)
        DBSession.add(moderators)
        DBSession.add(tagger)
        DBSession.add(bob)
        DBSession.add(alice)
        DBSession.flush()

        atb.delta_in.append(hcm)
        atb.delta_in.append(rcm)
        atb.delta_in.append(lars)
        atb.delta_in.append(jesko)
        hcm.delta_in.append(jesko)
        hcm.delta_in.append(rcm)
        rcm.delta_in.append(nikolai)
        rcm.delta_in.append(hanno)
        rcm.delta_in.append(ulrike)
        admins.delta_in.append(jesko)
        admins.delta_in.append(nikolai)
        moderators.delta_in.append(admins)
        moderators.delta_in.append(lars)
        tagger.delta_in.append(ulrike)
        tagger.delta_in.append(moderators)
        tagger.delta_in.append(admins)

        #Add another user
        other_usr = Usr(nickname='frehse', login='frehse', passwd='tester2', language='Deutsch', grp_id=frehse.id)
        DBSession.add(other_usr)
        DBSession.flush()
        #Add some persons person
        person1 = Person(name='Konrad Koenigsberger')
        person2 = Person(name='Falko Lorenz')
        DBSession.add(person1)
        DBSession.add(person2)
        DBSession.flush()
        #Add a Text
        T = Txt(title='Analysis 1', edition='1', isbn='1337', creator=adm_usr, language='Deutsch')
        T.author_list.append(person1)
        DBSession.add(
            Txt(title='Analysis 2', authors='Koenigsberger', edition='2', creator=adm_usr, language='English'))
        DBSession.add(
            Txt(title='Lineare Algebra 1', authors='Falko Lorenz', edition='1', creator=adm_usr, language='Deutsch'))
        DBSession.add(T)
        DBSession.flush()
        #Add Annotations to that text
        # A = Annotation(content='the $\infty$ should be an $n$', location='page 3, line 6', language='Deutsch')
        # A.creator = adm_usr
        # A.txts.append(T)
        # A.tags = 'remark'
        # DBSession.add(A)
        # B = Annotation(content='a second annotation', location='page 234, line 43', language='English')
        # B.creator = adm_usr
        # B.txts.append(T)
        # B.tags = 'unclear'
        # DBSession.add(B)
        # #DBSession.flush()
        # Create A TeX Header for our user
        # texh = TexHeader(name='MyDefaultHeader', content=r'\newcommand{\N}{\mathbb N}')
        # texh.creator = adm_usr
        # DBSession.add(texh)
        # DBSession.flush()
        # #Create a TeX Header for the other user
        # texhother = TexHeader(name='MyOtherUser', content=r'\newcommand{\Z}{\mathbb Z}')
        # texhother.creator = other_usr
        # DBSession.add(texhother)
        # DBSession.flush()
        # #Add several posts
        # post1 = Post(content='1) Cool Annotation. Look at my cool LaTeX Header: $\N$!', is_resolution=False,
        #              parent_id=False)
        # post1.creator = adm_usr
        # post1.annotation = A
        # post1.tex_header = texh
        # DBSession.add(post1)
        # DBSession.flush()
        # post2 = Post(content='2) In this post, my LaTeX Header is disabled. $\N$', is_resolution=False)
        # post2.creator = adm_usr
        # post2.parent_id = post1.id
        # DBSession.add(post2)
        # DBSession.flush()
        # post3 = Post(content='3) This post refers to my post 2).', is_resolution=False)
        # post3.creator = adm_usr
        # post3.parent_id = post2.id
        # DBSession.add(post3)
        # DBSession.flush()
        # post4 = Post(content='4) This post refers to my post 1).', is_resolution=False)
        # post4.creator = adm_usr
        # post4.parent_id = post1.id
        # DBSession.add(post4)
        # DBSession.flush()
        # post5 = Post(content='5) This post refers to my post 4).', is_resolution=False)
        # post5.creator = adm_usr
        # post5.parent_id = post4.id
        # DBSession.add(post5)
        # DBSession.flush()
        #
        # #Add some users, Txts and annotations for Authorization Testing
        # bob = Usr(nickname='bob', login='bob', passwd='bob', language='English', grp_id=bob.id)
        # DBSession.add(bob)
        # hartshorne = Person(name='Robin Hartshorne')
        # hefner = Person(name='Hugh Hefner')
        # DBSession.add(hartshorne)
        # DBSession.add(hefner)
        # DBSession.flush()
        # AlgGeo = Txt(title='Algebraic Geometry', edition='1', isbn='1337', creator=bob, language='English')
        # AlgGeo.author_list.append(hartshorne)
        # DBSession.add(AlgGeo)
        # Playboy = Txt(title='Playboy', edition='1', isbn='1337', creator=bob, language='English')
        # Playboy.author_list.append(hefner)
        # DBSession.add(Playboy)
        # DBSession.flush()
        # A = Annotation(content='the $\infty$ should be an $n$', title='world,world', location='page 3, line 6',
        #                language='English')
        # A.creator = bob
        # A.txts.append(AlgGeo)
        # A.tags = 'remark'
        # #DBSession.add(A)
        # B = Annotation(content='you cannot edit this', location='page 3, line 6', title='world,usr', language='English')
        # B.creator = bob
        # B.txts.append(AlgGeo)
        # B.tags = 'remark'
        # DBSession.add(B)
        # C = Annotation(content='this book sucks', location='page 3, line 6', language='English', title='usr, usr')
        # C.creator = bob
        # C.txts.append(AlgGeo)
        # C.tags = 'remark'
        # DBSession.add(C)
        # DBSession.flush()
        # AP = Annotation(content='the $\infty$ should be an $n$', title='world,world', location='page 3, line 6',
        #                 language='English')
        # AP.creator = bob
        # AP.txts.append(Playboy)
        # AP.tags = 'remark'
        # DBSession.add(AP)
        # BP = Annotation(content='you cannot edit this', location='page 3, line 6', title='world,usr',
        #                 language='English')
        # BP.creator = bob
        # BP.txts.append(Playboy)
        # BP.tags = 'remark'
        # DBSession.add(BP)
        # CP = Annotation(content='this book sucks', location='page 3, line 6', language='English', title='usr, usr')
        # CP.creator = bob
        # CP.txts.append(Playboy)
        # CP.tags = 'remark'
        # DBSession.add(CP)
        # DBSession.flush()
        #
        # alice = Usr(login='alice', nickname='alice', passwd='alice', language='English', grp_id=alice.id)
        # DBSession.add(alice)
        # hoermander = Person(name='Lars hoermander')
        # meyer = Person(name='Stephanie Meyer')
        # DBSession.add(hoermander)
        # DBSession.add(meyer)
        # DBSession.flush()
        # PDO = Txt(title='Linear Partial Differential Operators', edition='1', isbn='1337', creator=alice,
        #           language='English')
        # PDO.author_list.append(hoermander)
        # DBSession.add(PDO)
        # twilight = Txt(title='Twilight', edition='1', isbn='1337', creator=alice, language='English')
        # twilight.author_list.append(meyer)
        # DBSession.add(twilight)
        # DBSession.flush()
        # aA = Annotation(content='the $\infty$ should be an $n$', title='world,world', location='page 3, line 6',
        #                 language='English')
        # aA.creator = alice
        # aA.txts.append(PDO)
        # aA.tags = 'remark'
        # DBSession.add(aA)
        # aB = Annotation(content='you cannot edit this', location='page 3, line 6', title='world,usr',
        #                 language='English')
        # aB.creator = alice
        # aB.txts.append(PDO)
        # aB.tags = 'remark'
        # DBSession.add(aB)
        # aC = Annotation(content='this book sucks', location='page 3, line 6', language='English', title='usr, usr')
        # aC.creator = alice
        # aC.txts.append(PDO)
        # aC.tags = 'remark'
        # DBSession.add(aC)
        # DBSession.flush()
        # aAP = Annotation(content='the $\infty$ should be an $n$', title='world,world', location='page 3, line 6',
        #                  language='English')
        # aAP.creator = alice
        # aAP.txts.append(twilight)
        # aAP.tags = 'remark'
        # DBSession.add(aAP)
        # aBP = Annotation(content='you cannot edit this', location='page 3, line 6', title='world,usr',
        #                  language='English')
        # aBP.creator = alice
        # aBP.txts.append(twilight)
        # aBP.tags = 'remark'
        # DBSession.add(aBP)
        # aCP = Annotation(content='this book sucks', location='page 3, line 6', language='English', title='usr, usr')
        # aCP.creator = alice
        # aCP.txts.append(twilight)
        # aCP.tags = 'remark'
        # DBSession.add(aCP)
        # DBSession.flush()
