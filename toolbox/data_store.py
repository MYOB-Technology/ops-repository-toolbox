
# -*- coding: utf-8 -*-

# ########################## Copyrights and license ############################
#                                                                              #
# Copyright 2017 Song Jin <song.jin@myob.com>                                  #
#                                                                              #
# This file is part of myob-github-toolbox project.                            #
#                                                                              #
#                This module defines object models for DB                      #
#                                                                              #
# ##############################################################################

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class GithubUser(Base):
    __tablename__ = 'github_user'
    login = Column(String(100), primary_key=True, nullable=False)
    email = Column(String(250), nullable=True)
    full_name = Column(String(250), nullable=True)
    myob_membership = Column(Boolean, nullable=True)
    org = Column(String(250), nullable=True)
    two_fa_status = Column(Boolean, nullable=True)
    team = Column(String(250), nullable=True)


# class Employee(Base):
#     __tablename__ = 'employee'
#     email = Column(String(250), nullable=True)
#     full_name = Column(String(250), nullable=True)
#     group = Column(String(250), nullable=True)
#     active_status = Column(Boolean, nullable=True)



    # example how to link two tables together:

    # person_login = Column(String(100), ForeignKey('github_user.login'))
    # person = relationship(GithubUser)


# def init_db():
#     # create an engine that stores data in local dict as a file
#     engine = create_engine('sqlite:///toolbox.db')
#     Base.metadata.create_all(engine)



def upsert(args, entries, input):
    '''
        Business logic: get those who don't do 2FA && don't have valid names
        input: 'login':{'email':<email>, 'name':<name>, 'two_fa_status':<T/F>}
    '''
    if input['login'] in entries:

    else:

