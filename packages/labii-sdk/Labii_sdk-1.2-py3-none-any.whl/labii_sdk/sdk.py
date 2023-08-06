""" python api functions """
#from api import *
import requests
import json
import getpass
from labii_sdk.api_client import APIObject

class LabiiObject:
    api = None

    def __init__(self,
        organization__sid,
        base_url="https://www.labii.dev",
        email=None,
        password=None,
        token=None,
        user=None
    ):
        self.api = APIObject(base_url=base_url, email=email, password=password, token=token, organization__sid=organization__sid, user=user)
        self.Organization = self.APIResource(self, "organizations", "organization")
        self.People = self.APIResource(self, "organizations", "personnel")
        self.Team = self.APIResource(self, "organizations", "team")
        self.SAML = self.APIResource(self, "organizations", "saml")
        self.Project = self.APIResource(self, "projects", "project")
        self.ProjectMember = self.APIResource(self, "projects", "member")
        self.Table = self.APIResource(self, "tables", "table")
        self.Column = self.APIResource(self, "tables", "column")
        self.Section = self.APIResource(self, "tables", "section")
        self.Row = self.APIResource(self, "tables", "row")
        self.Cell = self.APIResource(self, "tables", "cell")
        self.Version = self.APIResource(self, "tables", "version")
        self.Visitor = self.APIResource(self, "tables", "visitor")

    class APIResource:
        """ abstract class """
        app = None
        object = None

        class Meta:
            abstract = True

        def __init__(self, instance, app, object):
            """
                - instance, the outer instance
            """
            self.instance = instance
            self.app = app
            self.object = object

        def create(self, data={}):
            """ Create a object """
            return self.instance.api.post(self.instance.api.get_list_url(self.app, self.object, serializer="detail"))

        def retrieve(self, sid):
            """ Return an object """
            return self.instance.api.get(self.instance.api.get_detail_url(self.app, self.object, sid=sid))

        def list(self, page=1, page_size=10, all=False, level="organization", serializer="list", query=""):
            """ Return list of objects """
            if all is True:
                url = self.instance.api.get_list_url(
                    self.app,
                    self.object,
                    sid=self.instance.api.organization__sid,
                    level=level,
                    serializer=serializer,
                    query=query
                )
                return self.instance.api.get(url, True)
            else:
                url = self.instance.api.get_list_url(
                    self.app,
                    self.object,
                    sid=self.instance.api.organization__sid,
                    level=level,
                    serializer=serializer,
                    query=f"page={page}&page_size={page_size}{'' if query == '' else '&'}{query}"
                )
                return self.instance.api.get(url)

        def modify(self, sid, data={}):
            """ Change one object """
            if self.can_patch:
                return self.instance.api.patch(self.instance.api.get_detail_url(self.app, self.object, sid=sid), data)
            else:
                print("Method not supported!")

        def delete(self, sid):
            """ Delete a object """
            self.instance.api.delete(self.instance.api.get_detail_url(self.app, self.object, sid=sid))
