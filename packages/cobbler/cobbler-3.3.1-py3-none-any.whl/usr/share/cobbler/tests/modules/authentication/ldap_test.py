import pytest
from cobbler.api import CobblerAPI
from cobbler.settings import Settings
from cobbler.modules.authentication import ldap

#@pytest.fixture(scope="class")
@pytest.fixture()
def api():
    return CobblerAPI()

@pytest.fixture()
def test_settings(api):
    settings = api.settings()
    settings.ldap_server = "localhost"
    settings.ldap_port = 389
    settings.ldap_base_dn = "dc=example,dc=com"
    settings.ldap_search_prefix = "uid="
    settings.ldap_anonymous_bind = True
    settings.ldap_reqcert = "hard"
    return settings

class TestLdap:
    @pytest.mark.parametrize("anonymous_bind, username, password", [
        (True, "test", "test")
    ])
    def test_anon_bind_positive(self, api, test_settings, anonymous_bind, username, password):
        # Arrange
        test_settings.ldap_anonymous_bind = anonymous_bind
        test_settings.ldap_tls = False

        # Act
        result = ldap.authenticate(api, username, password)

        # Assert
        assert result

    @pytest.mark.parametrize("anonymous_bind, username, password", [
        (True, "test", "bad")
    ])
    def test_anon_bind_negative(self, api, test_settings, anonymous_bind, username, password):
        # Arrange
        test_settings.ldap_anonymous_bind = anonymous_bind
        test_settings.ldap_tls = False

        # Act
        result = ldap.authenticate(api, username, password)

        # Assert
        assert not result

    @pytest.mark.parametrize("anonymous_bind, bind_user, bind_password, username, password", [
        (False, "uid=user,dc=example,dc=com", "test", "test", "test")
    ])
    def test_user_bind_positive(self, api, test_settings, anonymous_bind, bind_user, bind_password, username, password):
        # Arrange
        test_settings.ldap_anonymous_bind = anonymous_bind
        test_settings.ldap_search_bind_dn = bind_user
        test_settings.ldap_search_passwd = bind_password
        test_settings.ldap_tls = False

        # Act
        result = ldap.authenticate(api, username, password)

        # Assert
        assert result

    @pytest.mark.parametrize("anonymous_bind, bind_user, bind_password, username, password", [
        (False, "uid=user,dc=example,dc=com", "bad", "test", "test")
    ])
    def test_user_bind_negative(self, api, test_settings, anonymous_bind, bind_user, bind_password, username, password):
        # Arrange
        test_settings.ldap_anonymous_bind = anonymous_bind
        test_settings.ldap_search_bind_dn = bind_user
        test_settings.ldap_search_passwd = bind_password
        test_settings.ldap_tls = False

        # Act
        result = ldap.authenticate(api, username, password)

        # Assert
        assert not result

    @pytest.mark.parametrize("tls_cadir, tls_cert, tls_key", [
        ("/etc/ssl/certs",
         "/etc/ssl/ldap.crt",
         "/etc/ssl/ldap.key")
    ])
    def test_cadir_positive(self, api, test_settings, tls_cadir, tls_cert, tls_key):
        # Arrange
        test_settings.ldap_tls = True
        test_settings.ldap_tls_cacertdir = tls_cadir
        test_settings.ldap_tls_cacertfile = None
        test_settings.ldap_tls_certfile = tls_cert
        test_settings.ldap_tls_keyfile = tls_key

        # Act
        result = ldap.authenticate(api, "test", "test")

        # Assert
        assert result

    @pytest.mark.parametrize("tls_cadir, tls_cert, tls_key", [
        ("/etc/ssl/certs",
         "/etc/ssl/bad.crt",
         "/etc/ssl/bad.key")
    ])
    def test_cadir_negative(self, api, test_settings, tls_cadir, tls_cert, tls_key):
        # Arrange
        test_settings.ldap_tls = True
        test_settings.ldap_tls_cacertdir = tls_cadir
        test_settings.ldap_tls_cacertfile = None
        test_settings.ldap_tls_certfile = tls_cert
        test_settings.ldap_tls_keyfile = tls_key

        # Act
        result = ldap.authenticate(api, "test", "test")

        # Assert
        assert not result

    @pytest.mark.parametrize("tls_cafile, tls_cert, tls_key", [
        ("/etc/ssl/ca-slapd.crt",
         "/etc/ssl/ldap.crt",
         "/etc/ssl/ldap.key")
    ])
    def test_cafile_positive(self, api, test_settings, tls_cafile, tls_cert, tls_key):
        # Arrange
        test_settings.ldap_tls = True
        test_settings.ldap_tls_cacertdir = None
        test_settings.ldap_tls_cacertfile = tls_cafile
        test_settings.ldap_tls_certfile = tls_cert
        test_settings.ldap_tls_keyfile = tls_key

        # Act
        result = ldap.authenticate(api, "test", "test")

        # Assert
        assert result

    @pytest.mark.parametrize("tls_cafile, tls_cert, tls_key", [
        ("/etc/ssl/ca-slapd.crt",
         "/etc/ssl/bad.crt",
         "/etc/ssl/bad.key")
    ])
    def test_cafile_negative(self, api, test_settings, tls_cafile, tls_cert, tls_key):
        # Arrange
        test_settings.ldap_tls = True
        test_settings.ldap_tls_cacertdir = None
        test_settings.ldap_tls_cacertfile = tls_cafile
        test_settings.ldap_tls_certfile = tls_cert
        test_settings.ldap_tls_keyfile = tls_key

        # Act
        result = ldap.authenticate(api, "test", "test")

        # Assert
        assert not result

    @pytest.mark.parametrize("tls_cafile, tls_cert, tls_key", [
        ("/etc/ssl/ca-slapd.crt",
         "/etc/ssl/ldap.crt",
         "/etc/ssl/ldap.key")
    ])
    def test_ldaps_positive(self, api, test_settings, tls_cafile, tls_cert, tls_key):
        # Arrange
        test_settings.ldap_tls = False
        test_settings.ldap_port = 636
        test_settings.ldap_tls_cacertdir = None
        test_settings.ldap_tls_cacertfile = tls_cafile
        test_settings.ldap_tls_certfile = tls_cert
        test_settings.ldap_tls_keyfile = tls_key

        # Act
        result = ldap.authenticate(api, "test", "test")

        # Assert
        assert result

    @pytest.mark.parametrize("tls_cafile, tls_cert, tls_key", [
        ("/etc/ssl/ca-slapd.crt",
         "/etc/ssl/bad.crt",
         "/etc/ssl/bad.key")
    ])
    def test_ldaps_negative(self, api, test_settings, tls_cafile, tls_cert, tls_key):
        # Arrange
        test_settings.ldap_tls = False
        test_settings.ldap_port = 636
        test_settings.ldap_tls_cacertdir = None
        test_settings.ldap_tls_cacertfile = tls_cafile
        test_settings.ldap_tls_certfile = tls_cert
        test_settings.ldap_tls_keyfile = tls_key

        # Act & Assert
        with pytest.raises(ValueError):
            result = ldap.authenticate(api, "test", "test")
