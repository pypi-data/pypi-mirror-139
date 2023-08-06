# -*- coding: utf-8 -*-
"""Gaia Auth class file."""
import json


class Auth:
    """Gaia Auth class."""

    def __init__(self, gaia):
        """Initialize a class instance."""
        self.gaia = gaia

    def ad_ldap(self):
        """Return an authorized AD instance."""
        from bits.ldap.ad import AD
        settings = self.gaia.get_settings("ad_ldap")
        return AD(
            uri=settings.get("uri"),
            bind_dn=settings.get("bind_dn"),
            bind_pw=self.gaia.get_secret(settings.get("bind_pw_name")),
            base_dn=settings.get("base_dn"),
            server_type="ad",
            verbose=self.gaia.verbose,
        )

    def archibus(self):
        """Return an authorized Archibus instance."""
        from bits.gaia.archibus import Archibus
        settings = self.gaia.get_settings("archibus")
        client_id = self.gaia.get_secret(settings.get("client_id_name"))
        client_secret = self.gaia.get_secret(settings.get("client_secret_name"))
        return Archibus(
            client_id=client_id,
            client_secret=client_secret,
            auth_domain=settings.get("auth_domain"),
            base_url=settings.get("base_url"),
        )

    def atlassian(self):
        """Return an authorized Atlassian session."""
        from bits.gaia.atlassian import Atlassian
        settings = self.gaia.get_settings("atlassian")
        token = self.gaia.get_secret(settings.get("token_name"))
        username = settings.get("username")
        return Atlassian(username, token)

    def aws(self):
        """Return an authorized AWS session."""
        from bits.gaia.aws import AWS
        settings = self.gaia.get_settings("aws")
        access_key_id = self.gaia.get_secret(settings.get("access_key_id_name"))
        secret_access_key = self.gaia.get_secret(settings.get("secret_access_key_name"))
        return AWS(access_key_id, secret_access_key)

    def azure(self):
        """Return an authorized Azure session."""
        from bits.gaia.azure import Azure
        settings = self.gaia.get_settings("azure")
        client_id = self.gaia.get_secret(settings.get("client_id_name"))
        client_secret = self.gaia.get_secret(settings.get("client_secret_name"))
        tenant_id = settings.get("tenant_id")
        return Azure(client_id, client_secret, tenant_id)

    def bitsdb_mongo(self):
        """Return an authorized Mongo instance for BITSdb."""
        from bits.mongo import Mongo
        settings = self.gaia.get_settings("bitsdb_mongo")
        db = settings.get("db")
        host = settings.get("host")
        username = settings.get("username")
        password = self.gaia.get_secret(settings.get("password_name"))
        return Mongo(
            uri=f"mongodb://{username}:{password}@{host}/{db}",
            db=db,
            verbose=self.gaia.verbose,
        )

    def broadio_mysql(self):
        """Return an authorized MySQL instance for Broad.IO."""
        from bits.gaia.mysql import MySQL
        settings = self.gaia.get_settings("broadio_mysql")
        return MySQL(
            server=settings.get("server"),
            port=settings.get("port"),
            user=settings.get("user"),
            password=self.gaia.get_secret(settings.get("password_name")),
            db=settings.get("db"),
            verbose=self.gaia.verbose,
        )

    def calendar_mysql(self):
        """Return an authorized MySQL instance for Calendar."""
        from bits.gaia.mysql import MySQL
        settings = self.gaia.get_settings("calendar_mysql")
        return MySQL(
            server=settings.get("server"),
            port=settings.get("port"),
            user=settings.get("user"),
            password=self.gaia.get_secret(settings.get("password_name")),
            db=settings.get("db"),
            verbose=self.gaia.verbose,
        )

    def dialpad(self):
        """Return an authorized Dialpad instance for gaia."""
        from bits.dialpad import Dialpad
        settings = self.gaia.get_settings("dialpad")
        return Dialpad(
            token=self.gaia.get_secret(settings.get("token_name")),
        )

    def duo(self):
        """Return an authorized Duo instance for gaia."""
        from duo_client import Admin
        settings = self.gaia.get_settings("duo")
        return Admin(
            ikey=settings.get("integration_key"),
            skey=self.gaia.get_secret(settings.get("secret_key_name")),
            host=settings.get("hostname"),
        )

    def gaia_sftp(self):
        """Return an authorized SFTP instance for gaia."""
        from bits.sftp import SFTP
        settings = self.gaia.get_settings("gaia_ssh")
        return SFTP(
            host=settings.get("host"),
            path=settings.get("path"),
            username=settings.get("username"),
            key=self.gaia.get_secret(settings.get("key_name")),
        )

    def gaia_ssh(self):
        """Return an authorized SSH instance for Gaia."""
        from bits.gaia.ssh import SSH
        settings = self.gaia.get_settings("gaia_ssh")
        return SSH(
            host=settings.get("host"),
            user=settings.get("username"),
            key=self.gaia.get_secret(settings.get("key_name")),
            cli=settings.get("cli"),
        )

    def github(self):
        """Return a authorized Github instance for gaia."""
        from bits.github import GitHub
        settings = self.gaia.get_settings("github")
        return GitHub(
            token=self.gaia.get_secret(settings.get("token_name")),
            org=settings.get("organization"),
            owner_team=settings.get("owner_team"),
            role_team=settings.get("role_team"),
        )

    def google(self, scopes):
        """Return an authorized Google instance for gaia."""
        from bits.google import Google
        return Google(scopes=scopes)

    def google_admin(self, scopes):
        """Return an authorized Google instance for gaia."""
        from bits.google import Google
        settings = self.gaia.get_settings("google")
        return Google(
            scopes=scopes,
            service_account_info=json.loads(self.gaia.get_secret(settings.get("key_name"))),
        )

    def okta(self):
        """Return an authorized Okta instance for gaia."""
        from bits.gaia.okta import Okta
        settings = self.gaia.get_settings("okta")
        return Okta(
            token=self.gaia.get_secret(settings.get("token_name")),
            base_url=settings.get("base_url"),
        )

    def pagerduty(self):
        """Return an authorized PagerDuty instance for gaia."""
        from pdpyras import APISession
        settings = self.gaia.get_settings("pagerduty")
        return APISession(self.gaia.get_secret(settings.get("key_name")))

    def quay(self):
        """Return am authorized Quay instance for gaia."""
        from bits.quay import Quay
        settings = self.gaia.get_settings("quay")
        return Quay(
            token=self.gaia.get_secret(settings.get("token_name")),
            orgname=settings.get("organization"),
            role_team=settings.get("role_team"),
        )

    def people_mysql(self):
        """Return an authorized MySQL instance for People."""
        from bits.gaia.mysql import MySQL
        settings = self.gaia.get_settings("people_mysql")
        return MySQL(
            server=settings.get("server"),
            port=settings.get("port"),
            user=settings.get("user"),
            password=self.gaia.get_secret(settings.get("password_name")),
            db=settings.get("db"),
            verbose=self.gaia.verbose,
        )

    def redis(self):
        """Return an authorized redis instance."""
        from bits.gaia.redis import Redis
        settings = self.gaia.get_settings("redis")
        host = settings.get("host")
        port = settings.get("port", 6379)
        return Redis(host=host, port=port)

    def sap_mssql(self):
        """Return an authorized MSSQL instance for SAP datawarehouse."""
        from bits.mssql import MSSQL
        settings = self.gaia.get_settings("sap_mssql")
        server = settings.get("server")
        port = settings.get("port")
        return MSSQL(
            server=f"{server}:{port}",
            user=settings.get("user"),
            password=self.gaia.get_secret(settings.get("password_name")),
            database=settings.get("db"),
            verbose=self.gaia.verbose,
        )

    def sendgrid(self):
        """Return an authorized Sendgrid instance."""
        from bits.gaia.sendgrid import SendGrid
        settings = self.gaia.get_settings("sendgrid")
        api_key = self.gaia.get_secret(settings.get("api_key_name"))
        return SendGrid(api_key=api_key)

    def slack_admin_user(self):
        """Return an authorized Slack Admin instance with a user token."""
        from bits.gaia.slack import Slack
        settings = self.gaia.get_settings("slack_admin")
        token = self.gaia.get_secret(settings.get("user_token_name"))
        return Slack(token=token)

    def slack_broadbits_bot(self):
        """Return an authorized broadbits Slack Workspace instance with a bot token."""
        from bits.gaia.slack import Slack
        settings = self.gaia.get_settings("slack_broadbits")
        token = self.gaia.get_secret(settings.get("bot_token_name"))
        return Slack(token=token)

    def slack_broadbits_user(self):
        """Return an authorized broadbits Slack Workspace instance with a user token."""
        from bits.gaia.slack import Slack
        settings = self.gaia.get_settings("slack_broadbits")
        token = self.gaia.get_secret(settings.get("user_token_name"))
        return Slack(token=token)

    def slack_broadinstitute_bot(self):
        """Return an authorized broadinstitute Slack Workspace instance with a bot token."""
        from bits.gaia.slack import Slack
        settings = self.gaia.get_settings("slack_broadinstitute")
        token = self.gaia.get_secret(settings.get("bot_token_name"))
        return Slack(token=token)

    def slack_broadinstitute_user(self):
        """Return an authorized broadinstitute Slack Workspace instance with a user token."""
        from bits.gaia.slack import Slack
        settings = self.gaia.get_settings("slack_broadinstitute")
        token = self.gaia.get_secret(settings.get("user_token_name"))
        return Slack(token=token)

    def space_mysql(self):
        """Return an authorized MySQL instance for Space."""
        from bits.gaia.mysql import MySQL
        settings = self.gaia.get_settings("space_mysql")
        return MySQL(
            server=settings.get("server"),
            port=settings.get("port"),
            user=settings.get("user"),
            password=self.gaia.get_secret(settings.get("password_name")),
            db=settings.get("db"),
            verbose=self.gaia.verbose,
        )

    def workday(self):
        """Return an authorized Workday instance.."""
        from bits.gaia.workday import Workday
        config = self.gaia.get_settings("workday_people_feed")
        return Workday(
            base_url=config.get("base_url"),
            username=config.get("username"),
            password=self.gaia.get_secret(config.get("password_name")),
            tenant=config.get("tenant"),
            version=config.get("version"),
        )
