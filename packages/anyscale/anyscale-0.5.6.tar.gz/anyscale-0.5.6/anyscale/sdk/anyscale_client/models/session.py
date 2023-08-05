# coding: utf-8

"""
    Anyscale API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from anyscale_client.configuration import Configuration


class Session(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'name': 'str',
        'project_id': 'str',
        'cloud_id': 'str',
        'cluster_config': 'str',
        'build_id': 'str',
        'compute_template_id': 'str',
        'idle_timeout': 'int',
        'uses_app_config': 'bool',
        'allow_public_internet_traffic': 'bool',
        'id': 'str',
        'state': 'SessionState',
        'pending_state': 'SessionState',
        'state_data': 'SessionStateData',
        'creator_id': 'str',
        'created_at': 'datetime',
        'webterminal_auth_url': 'str',
        'metrics_dashboard_url': 'str',
        'connect_url': 'str',
        'jupyter_notebook_url': 'str',
        'ray_dashboard_url': 'str',
        'access_token': 'str',
        'service_proxy_url': 'str',
        'tensorboard_available': 'bool',
        'cluster_config_last_modified_at': 'datetime',
        'host_name': 'str',
        'head_node_ip': 'str',
        'ssh_authorized_keys': 'list[str]',
        'ssh_private_key': 'str',
        'anyscaled_config': 'str',
        'anyscaled_config_generated_at': 'datetime',
        'default_build_id': 'str',
        'idle_timeout_last_activity_at': 'datetime',
        'ray_version': 'str',
        'ray_version_last_updated_at': 'datetime'
    }

    attribute_map = {
        'name': 'name',
        'project_id': 'project_id',
        'cloud_id': 'cloud_id',
        'cluster_config': 'cluster_config',
        'build_id': 'build_id',
        'compute_template_id': 'compute_template_id',
        'idle_timeout': 'idle_timeout',
        'uses_app_config': 'uses_app_config',
        'allow_public_internet_traffic': 'allow_public_internet_traffic',
        'id': 'id',
        'state': 'state',
        'pending_state': 'pending_state',
        'state_data': 'state_data',
        'creator_id': 'creator_id',
        'created_at': 'created_at',
        'webterminal_auth_url': 'webterminal_auth_url',
        'metrics_dashboard_url': 'metrics_dashboard_url',
        'connect_url': 'connect_url',
        'jupyter_notebook_url': 'jupyter_notebook_url',
        'ray_dashboard_url': 'ray_dashboard_url',
        'access_token': 'access_token',
        'service_proxy_url': 'service_proxy_url',
        'tensorboard_available': 'tensorboard_available',
        'cluster_config_last_modified_at': 'cluster_config_last_modified_at',
        'host_name': 'host_name',
        'head_node_ip': 'head_node_ip',
        'ssh_authorized_keys': 'ssh_authorized_keys',
        'ssh_private_key': 'ssh_private_key',
        'anyscaled_config': 'anyscaled_config',
        'anyscaled_config_generated_at': 'anyscaled_config_generated_at',
        'default_build_id': 'default_build_id',
        'idle_timeout_last_activity_at': 'idle_timeout_last_activity_at',
        'ray_version': 'ray_version',
        'ray_version_last_updated_at': 'ray_version_last_updated_at'
    }

    def __init__(self, name=None, project_id=None, cloud_id=None, cluster_config=None, build_id=None, compute_template_id=None, idle_timeout=120, uses_app_config=False, allow_public_internet_traffic=False, id=None, state=None, pending_state=None, state_data=None, creator_id=None, created_at=None, webterminal_auth_url=None, metrics_dashboard_url=None, connect_url=None, jupyter_notebook_url=None, ray_dashboard_url=None, access_token=None, service_proxy_url=None, tensorboard_available=None, cluster_config_last_modified_at=None, host_name=None, head_node_ip=None, ssh_authorized_keys=None, ssh_private_key=None, anyscaled_config=None, anyscaled_config_generated_at=None, default_build_id=None, idle_timeout_last_activity_at=None, ray_version=None, ray_version_last_updated_at=None, local_vars_configuration=None):  # noqa: E501
        """Session - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._project_id = None
        self._cloud_id = None
        self._cluster_config = None
        self._build_id = None
        self._compute_template_id = None
        self._idle_timeout = None
        self._uses_app_config = None
        self._allow_public_internet_traffic = None
        self._id = None
        self._state = None
        self._pending_state = None
        self._state_data = None
        self._creator_id = None
        self._created_at = None
        self._webterminal_auth_url = None
        self._metrics_dashboard_url = None
        self._connect_url = None
        self._jupyter_notebook_url = None
        self._ray_dashboard_url = None
        self._access_token = None
        self._service_proxy_url = None
        self._tensorboard_available = None
        self._cluster_config_last_modified_at = None
        self._host_name = None
        self._head_node_ip = None
        self._ssh_authorized_keys = None
        self._ssh_private_key = None
        self._anyscaled_config = None
        self._anyscaled_config_generated_at = None
        self._default_build_id = None
        self._idle_timeout_last_activity_at = None
        self._ray_version = None
        self._ray_version_last_updated_at = None
        self.discriminator = None

        self.name = name
        self.project_id = project_id
        self.cloud_id = cloud_id
        self.cluster_config = cluster_config
        if build_id is not None:
            self.build_id = build_id
        if compute_template_id is not None:
            self.compute_template_id = compute_template_id
        if idle_timeout is not None:
            self.idle_timeout = idle_timeout
        if uses_app_config is not None:
            self.uses_app_config = uses_app_config
        if allow_public_internet_traffic is not None:
            self.allow_public_internet_traffic = allow_public_internet_traffic
        self.id = id
        self.state = state
        if pending_state is not None:
            self.pending_state = pending_state
        if state_data is not None:
            self.state_data = state_data
        self.creator_id = creator_id
        self.created_at = created_at
        if webterminal_auth_url is not None:
            self.webterminal_auth_url = webterminal_auth_url
        if metrics_dashboard_url is not None:
            self.metrics_dashboard_url = metrics_dashboard_url
        if connect_url is not None:
            self.connect_url = connect_url
        if jupyter_notebook_url is not None:
            self.jupyter_notebook_url = jupyter_notebook_url
        if ray_dashboard_url is not None:
            self.ray_dashboard_url = ray_dashboard_url
        self.access_token = access_token
        if service_proxy_url is not None:
            self.service_proxy_url = service_proxy_url
        self.tensorboard_available = tensorboard_available
        self.cluster_config_last_modified_at = cluster_config_last_modified_at
        if host_name is not None:
            self.host_name = host_name
        if head_node_ip is not None:
            self.head_node_ip = head_node_ip
        self.ssh_authorized_keys = ssh_authorized_keys
        self.ssh_private_key = ssh_private_key
        if anyscaled_config is not None:
            self.anyscaled_config = anyscaled_config
        if anyscaled_config_generated_at is not None:
            self.anyscaled_config_generated_at = anyscaled_config_generated_at
        if default_build_id is not None:
            self.default_build_id = default_build_id
        if idle_timeout_last_activity_at is not None:
            self.idle_timeout_last_activity_at = idle_timeout_last_activity_at
        if ray_version is not None:
            self.ray_version = ray_version
        if ray_version_last_updated_at is not None:
            self.ray_version_last_updated_at = ray_version_last_updated_at

    @property
    def name(self):
        """Gets the name of this Session.  # noqa: E501

        Name of the session to be created.  # noqa: E501

        :return: The name of this Session.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Session.

        Name of the session to be created.  # noqa: E501

        :param name: The name of this Session.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def project_id(self):
        """Gets the project_id of this Session.  # noqa: E501

        Project that the session will be created in.  # noqa: E501

        :return: The project_id of this Session.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this Session.

        Project that the session will be created in.  # noqa: E501

        :param project_id: The project_id of this Session.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and project_id is None:  # noqa: E501
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def cloud_id(self):
        """Gets the cloud_id of this Session.  # noqa: E501

        Cloud that the session will use.  # noqa: E501

        :return: The cloud_id of this Session.  # noqa: E501
        :rtype: str
        """
        return self._cloud_id

    @cloud_id.setter
    def cloud_id(self, cloud_id):
        """Sets the cloud_id of this Session.

        Cloud that the session will use.  # noqa: E501

        :param cloud_id: The cloud_id of this Session.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and cloud_id is None:  # noqa: E501
            raise ValueError("Invalid value for `cloud_id`, must not be `None`")  # noqa: E501

        self._cloud_id = cloud_id

    @property
    def cluster_config(self):
        """Gets the cluster_config of this Session.  # noqa: E501

        Cluster config that the session can later be started with.  # noqa: E501

        :return: The cluster_config of this Session.  # noqa: E501
        :rtype: str
        """
        return self._cluster_config

    @cluster_config.setter
    def cluster_config(self, cluster_config):
        """Sets the cluster_config of this Session.

        Cluster config that the session can later be started with.  # noqa: E501

        :param cluster_config: The cluster_config of this Session.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and cluster_config is None:  # noqa: E501
            raise ValueError("Invalid value for `cluster_config`, must not be `None`")  # noqa: E501

        self._cluster_config = cluster_config

    @property
    def build_id(self):
        """Gets the build_id of this Session.  # noqa: E501

        ID of the Build that this session was started with.  # noqa: E501

        :return: The build_id of this Session.  # noqa: E501
        :rtype: str
        """
        return self._build_id

    @build_id.setter
    def build_id(self, build_id):
        """Sets the build_id of this Session.

        ID of the Build that this session was started with.  # noqa: E501

        :param build_id: The build_id of this Session.  # noqa: E501
        :type: str
        """

        self._build_id = build_id

    @property
    def compute_template_id(self):
        """Gets the compute_template_id of this Session.  # noqa: E501

        ID of the compute template that this session was started with.  # noqa: E501

        :return: The compute_template_id of this Session.  # noqa: E501
        :rtype: str
        """
        return self._compute_template_id

    @compute_template_id.setter
    def compute_template_id(self, compute_template_id):
        """Sets the compute_template_id of this Session.

        ID of the compute template that this session was started with.  # noqa: E501

        :param compute_template_id: The compute_template_id of this Session.  # noqa: E501
        :type: str
        """

        self._compute_template_id = compute_template_id

    @property
    def idle_timeout(self):
        """Gets the idle_timeout of this Session.  # noqa: E501

        Idle timeout (in minutes), after which the session is stopped. Idle time is defined as the time during which a session is not running a user command (through 'anyscale exec' or the Web UI), and does not have an attached driver. Time spent running Jupyter commands, or commands run through ssh, is still considered 'idle'.  # noqa: E501

        :return: The idle_timeout of this Session.  # noqa: E501
        :rtype: int
        """
        return self._idle_timeout

    @idle_timeout.setter
    def idle_timeout(self, idle_timeout):
        """Sets the idle_timeout of this Session.

        Idle timeout (in minutes), after which the session is stopped. Idle time is defined as the time during which a session is not running a user command (through 'anyscale exec' or the Web UI), and does not have an attached driver. Time spent running Jupyter commands, or commands run through ssh, is still considered 'idle'.  # noqa: E501

        :param idle_timeout: The idle_timeout of this Session.  # noqa: E501
        :type: int
        """

        self._idle_timeout = idle_timeout

    @property
    def uses_app_config(self):
        """Gets the uses_app_config of this Session.  # noqa: E501

        Whether or not the session uses app config. If true, it means this is not a legacy session started with cluster yaml.  # noqa: E501

        :return: The uses_app_config of this Session.  # noqa: E501
        :rtype: bool
        """
        return self._uses_app_config

    @uses_app_config.setter
    def uses_app_config(self, uses_app_config):
        """Sets the uses_app_config of this Session.

        Whether or not the session uses app config. If true, it means this is not a legacy session started with cluster yaml.  # noqa: E501

        :param uses_app_config: The uses_app_config of this Session.  # noqa: E501
        :type: bool
        """

        self._uses_app_config = uses_app_config

    @property
    def allow_public_internet_traffic(self):
        """Gets the allow_public_internet_traffic of this Session.  # noqa: E501

        Whether public internet traffic can access Serve endpoints or if an authentication token is required.  # noqa: E501

        :return: The allow_public_internet_traffic of this Session.  # noqa: E501
        :rtype: bool
        """
        return self._allow_public_internet_traffic

    @allow_public_internet_traffic.setter
    def allow_public_internet_traffic(self, allow_public_internet_traffic):
        """Sets the allow_public_internet_traffic of this Session.

        Whether public internet traffic can access Serve endpoints or if an authentication token is required.  # noqa: E501

        :param allow_public_internet_traffic: The allow_public_internet_traffic of this Session.  # noqa: E501
        :type: bool
        """

        self._allow_public_internet_traffic = allow_public_internet_traffic

    @property
    def id(self):
        """Gets the id of this Session.  # noqa: E501

        Server assigned unique identifier.  # noqa: E501

        :return: The id of this Session.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Session.

        Server assigned unique identifier.  # noqa: E501

        :param id: The id of this Session.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def state(self):
        """Gets the state of this Session.  # noqa: E501

        Current state of the Session.  # noqa: E501

        :return: The state of this Session.  # noqa: E501
        :rtype: SessionState
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this Session.

        Current state of the Session.  # noqa: E501

        :param state: The state of this Session.  # noqa: E501
        :type: SessionState
        """
        if self.local_vars_configuration.client_side_validation and state is None:  # noqa: E501
            raise ValueError("Invalid value for `state`, must not be `None`")  # noqa: E501

        self._state = state

    @property
    def pending_state(self):
        """Gets the pending_state of this Session.  # noqa: E501

        Pending state of the Session if a state transition has been requested.  # noqa: E501

        :return: The pending_state of this Session.  # noqa: E501
        :rtype: SessionState
        """
        return self._pending_state

    @pending_state.setter
    def pending_state(self, pending_state):
        """Sets the pending_state of this Session.

        Pending state of the Session if a state transition has been requested.  # noqa: E501

        :param pending_state: The pending_state of this Session.  # noqa: E501
        :type: SessionState
        """

        self._pending_state = pending_state

    @property
    def state_data(self):
        """Gets the state_data of this Session.  # noqa: E501

        Additional information about the current state  # noqa: E501

        :return: The state_data of this Session.  # noqa: E501
        :rtype: SessionStateData
        """
        return self._state_data

    @state_data.setter
    def state_data(self, state_data):
        """Sets the state_data of this Session.

        Additional information about the current state  # noqa: E501

        :param state_data: The state_data of this Session.  # noqa: E501
        :type: SessionStateData
        """

        self._state_data = state_data

    @property
    def creator_id(self):
        """Gets the creator_id of this Session.  # noqa: E501

        Identifier of user who created the Session.  # noqa: E501

        :return: The creator_id of this Session.  # noqa: E501
        :rtype: str
        """
        return self._creator_id

    @creator_id.setter
    def creator_id(self, creator_id):
        """Sets the creator_id of this Session.

        Identifier of user who created the Session.  # noqa: E501

        :param creator_id: The creator_id of this Session.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and creator_id is None:  # noqa: E501
            raise ValueError("Invalid value for `creator_id`, must not be `None`")  # noqa: E501

        self._creator_id = creator_id

    @property
    def created_at(self):
        """Gets the created_at of this Session.  # noqa: E501

        Time at which session was created.  # noqa: E501

        :return: The created_at of this Session.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Session.

        Time at which session was created.  # noqa: E501

        :param created_at: The created_at of this Session.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def webterminal_auth_url(self):
        """Gets the webterminal_auth_url of this Session.  # noqa: E501

        URL to authenticate with the webterminalThis field will only be populated after the Session finishes starting.  # noqa: E501

        :return: The webterminal_auth_url of this Session.  # noqa: E501
        :rtype: str
        """
        return self._webterminal_auth_url

    @webterminal_auth_url.setter
    def webterminal_auth_url(self, webterminal_auth_url):
        """Sets the webterminal_auth_url of this Session.

        URL to authenticate with the webterminalThis field will only be populated after the Session finishes starting.  # noqa: E501

        :param webterminal_auth_url: The webterminal_auth_url of this Session.  # noqa: E501
        :type: str
        """

        self._webterminal_auth_url = webterminal_auth_url

    @property
    def metrics_dashboard_url(self):
        """Gets the metrics_dashboard_url of this Session.  # noqa: E501

        URL for Grafana (metrics) dashboard for this Session. This field will only be populated after the Session finishes starting.  # noqa: E501

        :return: The metrics_dashboard_url of this Session.  # noqa: E501
        :rtype: str
        """
        return self._metrics_dashboard_url

    @metrics_dashboard_url.setter
    def metrics_dashboard_url(self, metrics_dashboard_url):
        """Sets the metrics_dashboard_url of this Session.

        URL for Grafana (metrics) dashboard for this Session. This field will only be populated after the Session finishes starting.  # noqa: E501

        :param metrics_dashboard_url: The metrics_dashboard_url of this Session.  # noqa: E501
        :type: str
        """

        self._metrics_dashboard_url = metrics_dashboard_url

    @property
    def connect_url(self):
        """Gets the connect_url of this Session.  # noqa: E501

        URL for Anyscale connect for this Session. This field will only be populated after the Session finishes starting.  # noqa: E501

        :return: The connect_url of this Session.  # noqa: E501
        :rtype: str
        """
        return self._connect_url

    @connect_url.setter
    def connect_url(self, connect_url):
        """Sets the connect_url of this Session.

        URL for Anyscale connect for this Session. This field will only be populated after the Session finishes starting.  # noqa: E501

        :param connect_url: The connect_url of this Session.  # noqa: E501
        :type: str
        """

        self._connect_url = connect_url

    @property
    def jupyter_notebook_url(self):
        """Gets the jupyter_notebook_url of this Session.  # noqa: E501

        URL for Jupyter Lab for this Session. This field will only be populated after the Session finishes starting.  # noqa: E501

        :return: The jupyter_notebook_url of this Session.  # noqa: E501
        :rtype: str
        """
        return self._jupyter_notebook_url

    @jupyter_notebook_url.setter
    def jupyter_notebook_url(self, jupyter_notebook_url):
        """Sets the jupyter_notebook_url of this Session.

        URL for Jupyter Lab for this Session. This field will only be populated after the Session finishes starting.  # noqa: E501

        :param jupyter_notebook_url: The jupyter_notebook_url of this Session.  # noqa: E501
        :type: str
        """

        self._jupyter_notebook_url = jupyter_notebook_url

    @property
    def ray_dashboard_url(self):
        """Gets the ray_dashboard_url of this Session.  # noqa: E501

        URL for Ray dashboard for this Session. This field will only be populated after the Session finishes starting.  # noqa: E501

        :return: The ray_dashboard_url of this Session.  # noqa: E501
        :rtype: str
        """
        return self._ray_dashboard_url

    @ray_dashboard_url.setter
    def ray_dashboard_url(self, ray_dashboard_url):
        """Sets the ray_dashboard_url of this Session.

        URL for Ray dashboard for this Session. This field will only be populated after the Session finishes starting.  # noqa: E501

        :param ray_dashboard_url: The ray_dashboard_url of this Session.  # noqa: E501
        :type: str
        """

        self._ray_dashboard_url = ray_dashboard_url

    @property
    def access_token(self):
        """Gets the access_token of this Session.  # noqa: E501

        Access token for web based services (e.g. jupyter, tensorboard, etc). This field will be populated when the web based services are available after the Session finishes starting.  # noqa: E501

        :return: The access_token of this Session.  # noqa: E501
        :rtype: str
        """
        return self._access_token

    @access_token.setter
    def access_token(self, access_token):
        """Sets the access_token of this Session.

        Access token for web based services (e.g. jupyter, tensorboard, etc). This field will be populated when the web based services are available after the Session finishes starting.  # noqa: E501

        :param access_token: The access_token of this Session.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and access_token is None:  # noqa: E501
            raise ValueError("Invalid value for `access_token`, must not be `None`")  # noqa: E501

        self._access_token = access_token

    @property
    def service_proxy_url(self):
        """Gets the service_proxy_url of this Session.  # noqa: E501

        Link to the web services proxy (e.g. jupyter, tensorboard, etc). This field will be populated when the web based services are available after the Session finishes starting.  # noqa: E501

        :return: The service_proxy_url of this Session.  # noqa: E501
        :rtype: str
        """
        return self._service_proxy_url

    @service_proxy_url.setter
    def service_proxy_url(self, service_proxy_url):
        """Sets the service_proxy_url of this Session.

        Link to the web services proxy (e.g. jupyter, tensorboard, etc). This field will be populated when the web based services are available after the Session finishes starting.  # noqa: E501

        :param service_proxy_url: The service_proxy_url of this Session.  # noqa: E501
        :type: str
        """

        self._service_proxy_url = service_proxy_url

    @property
    def tensorboard_available(self):
        """Gets the tensorboard_available of this Session.  # noqa: E501

        Represents whether Tensorboard is available.  # noqa: E501

        :return: The tensorboard_available of this Session.  # noqa: E501
        :rtype: bool
        """
        return self._tensorboard_available

    @tensorboard_available.setter
    def tensorboard_available(self, tensorboard_available):
        """Sets the tensorboard_available of this Session.

        Represents whether Tensorboard is available.  # noqa: E501

        :param tensorboard_available: The tensorboard_available of this Session.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and tensorboard_available is None:  # noqa: E501
            raise ValueError("Invalid value for `tensorboard_available`, must not be `None`")  # noqa: E501

        self._tensorboard_available = tensorboard_available

    @property
    def cluster_config_last_modified_at(self):
        """Gets the cluster_config_last_modified_at of this Session.  # noqa: E501

        Time when the cluster config for the Session was last modified.  # noqa: E501

        :return: The cluster_config_last_modified_at of this Session.  # noqa: E501
        :rtype: datetime
        """
        return self._cluster_config_last_modified_at

    @cluster_config_last_modified_at.setter
    def cluster_config_last_modified_at(self, cluster_config_last_modified_at):
        """Sets the cluster_config_last_modified_at of this Session.

        Time when the cluster config for the Session was last modified.  # noqa: E501

        :param cluster_config_last_modified_at: The cluster_config_last_modified_at of this Session.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and cluster_config_last_modified_at is None:  # noqa: E501
            raise ValueError("Invalid value for `cluster_config_last_modified_at`, must not be `None`")  # noqa: E501

        self._cluster_config_last_modified_at = cluster_config_last_modified_at

    @property
    def host_name(self):
        """Gets the host_name of this Session.  # noqa: E501

        URL for the head node of the cluster. This field will be populated after the cluster finishes starting.  # noqa: E501

        :return: The host_name of this Session.  # noqa: E501
        :rtype: str
        """
        return self._host_name

    @host_name.setter
    def host_name(self, host_name):
        """Sets the host_name of this Session.

        URL for the head node of the cluster. This field will be populated after the cluster finishes starting.  # noqa: E501

        :param host_name: The host_name of this Session.  # noqa: E501
        :type: str
        """

        self._host_name = host_name

    @property
    def head_node_ip(self):
        """Gets the head_node_ip of this Session.  # noqa: E501

        Head IP of the Session. This field will be populated after the cluster finishes starting.  # noqa: E501

        :return: The head_node_ip of this Session.  # noqa: E501
        :rtype: str
        """
        return self._head_node_ip

    @head_node_ip.setter
    def head_node_ip(self, head_node_ip):
        """Sets the head_node_ip of this Session.

        Head IP of the Session. This field will be populated after the cluster finishes starting.  # noqa: E501

        :param head_node_ip: The head_node_ip of this Session.  # noqa: E501
        :type: str
        """

        self._head_node_ip = head_node_ip

    @property
    def ssh_authorized_keys(self):
        """Gets the ssh_authorized_keys of this Session.  # noqa: E501

        Serialized SSH Public Keys to be placed in the machine's authorized_keys.  # noqa: E501

        :return: The ssh_authorized_keys of this Session.  # noqa: E501
        :rtype: list[str]
        """
        return self._ssh_authorized_keys

    @ssh_authorized_keys.setter
    def ssh_authorized_keys(self, ssh_authorized_keys):
        """Sets the ssh_authorized_keys of this Session.

        Serialized SSH Public Keys to be placed in the machine's authorized_keys.  # noqa: E501

        :param ssh_authorized_keys: The ssh_authorized_keys of this Session.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and ssh_authorized_keys is None:  # noqa: E501
            raise ValueError("Invalid value for `ssh_authorized_keys`, must not be `None`")  # noqa: E501

        self._ssh_authorized_keys = ssh_authorized_keys

    @property
    def ssh_private_key(self):
        """Gets the ssh_private_key of this Session.  # noqa: E501

        SSH Private key that can be used to access the session's servers.  # noqa: E501

        :return: The ssh_private_key of this Session.  # noqa: E501
        :rtype: str
        """
        return self._ssh_private_key

    @ssh_private_key.setter
    def ssh_private_key(self, ssh_private_key):
        """Sets the ssh_private_key of this Session.

        SSH Private key that can be used to access the session's servers.  # noqa: E501

        :param ssh_private_key: The ssh_private_key of this Session.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and ssh_private_key is None:  # noqa: E501
            raise ValueError("Invalid value for `ssh_private_key`, must not be `None`")  # noqa: E501

        self._ssh_private_key = ssh_private_key

    @property
    def anyscaled_config(self):
        """Gets the anyscaled_config of this Session.  # noqa: E501

        Serialized AnyscaleD config that is general to head and worker nodes.  # noqa: E501

        :return: The anyscaled_config of this Session.  # noqa: E501
        :rtype: str
        """
        return self._anyscaled_config

    @anyscaled_config.setter
    def anyscaled_config(self, anyscaled_config):
        """Sets the anyscaled_config of this Session.

        Serialized AnyscaleD config that is general to head and worker nodes.  # noqa: E501

        :param anyscaled_config: The anyscaled_config of this Session.  # noqa: E501
        :type: str
        """

        self._anyscaled_config = anyscaled_config

    @property
    def anyscaled_config_generated_at(self):
        """Gets the anyscaled_config_generated_at of this Session.  # noqa: E501

        Time when AnyscaleD config was generated at.  # noqa: E501

        :return: The anyscaled_config_generated_at of this Session.  # noqa: E501
        :rtype: datetime
        """
        return self._anyscaled_config_generated_at

    @anyscaled_config_generated_at.setter
    def anyscaled_config_generated_at(self, anyscaled_config_generated_at):
        """Sets the anyscaled_config_generated_at of this Session.

        Time when AnyscaleD config was generated at.  # noqa: E501

        :param anyscaled_config_generated_at: The anyscaled_config_generated_at of this Session.  # noqa: E501
        :type: datetime
        """

        self._anyscaled_config_generated_at = anyscaled_config_generated_at

    @property
    def default_build_id(self):
        """Gets the default_build_id of this Session.  # noqa: E501

        Default build id used for the session. Only not null when using default builds.  # noqa: E501

        :return: The default_build_id of this Session.  # noqa: E501
        :rtype: str
        """
        return self._default_build_id

    @default_build_id.setter
    def default_build_id(self, default_build_id):
        """Sets the default_build_id of this Session.

        Default build id used for the session. Only not null when using default builds.  # noqa: E501

        :param default_build_id: The default_build_id of this Session.  # noqa: E501
        :type: str
        """

        self._default_build_id = default_build_id

    @property
    def idle_timeout_last_activity_at(self):
        """Gets the idle_timeout_last_activity_at of this Session.  # noqa: E501

        The time when this session started idling. If idle_timeout is enabled and this value is None, then this session is still active.  # noqa: E501

        :return: The idle_timeout_last_activity_at of this Session.  # noqa: E501
        :rtype: datetime
        """
        return self._idle_timeout_last_activity_at

    @idle_timeout_last_activity_at.setter
    def idle_timeout_last_activity_at(self, idle_timeout_last_activity_at):
        """Sets the idle_timeout_last_activity_at of this Session.

        The time when this session started idling. If idle_timeout is enabled and this value is None, then this session is still active.  # noqa: E501

        :param idle_timeout_last_activity_at: The idle_timeout_last_activity_at of this Session.  # noqa: E501
        :type: datetime
        """

        self._idle_timeout_last_activity_at = idle_timeout_last_activity_at

    @property
    def ray_version(self):
        """Gets the ray_version of this Session.  # noqa: E501

        The last known ray version running on this cluster.  # noqa: E501

        :return: The ray_version of this Session.  # noqa: E501
        :rtype: str
        """
        return self._ray_version

    @ray_version.setter
    def ray_version(self, ray_version):
        """Sets the ray_version of this Session.

        The last known ray version running on this cluster.  # noqa: E501

        :param ray_version: The ray_version of this Session.  # noqa: E501
        :type: str
        """

        self._ray_version = ray_version

    @property
    def ray_version_last_updated_at(self):
        """Gets the ray_version_last_updated_at of this Session.  # noqa: E501

        The time in which the ray version of this was updated.  # noqa: E501

        :return: The ray_version_last_updated_at of this Session.  # noqa: E501
        :rtype: datetime
        """
        return self._ray_version_last_updated_at

    @ray_version_last_updated_at.setter
    def ray_version_last_updated_at(self, ray_version_last_updated_at):
        """Sets the ray_version_last_updated_at of this Session.

        The time in which the ray version of this was updated.  # noqa: E501

        :param ray_version_last_updated_at: The ray_version_last_updated_at of this Session.  # noqa: E501
        :type: datetime
        """

        self._ray_version_last_updated_at = ray_version_last_updated_at

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Session):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Session):
            return True

        return self.to_dict() != other.to_dict()
