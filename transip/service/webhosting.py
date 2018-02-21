from transip.client import Client, MODE_RO, MODE_RW
from suds.sudsobject import Object as SudsObject


class WebhostingPackage(SudsObject):

    def __init__(self, name, description, price, renewalPrice):
        super(WebhostingPackage, self).__init__()

        self.name = name
        self.description = description
        self.price = price
        self.renewalPrice = renewalPrice


class WebHost(SudsObject):

    def __init__(self, domainName, cronjobs=None, mailBoxes=None, dbs=None, mailForwards=None, subDomains=None):
        super(WebHost, self).__init__()

        self.domainName = domainName
        self.cronjobs = cronjobs
        self.mailBoxes = mailBoxes
        self.dbs = dbs
        self.mailForwards = mailForwards
        self.subDomains = subDomains


class MailBox(SudsObject):
    SPAMCHECKER_STRENGTH_AVERAGE = 'AVERAGE'
    SPAMCHECKER_STRENGTH_OFF = 'OFF'
    SPAMCHECKER_STRENGTH_LOW = 'LOW'
    SPAMCHECKER_STRENGTH_HIGH = 'HIGH'

    address = None,
    spamCheckerStrength = SPAMCHECKER_STRENGTH_AVERAGE,
    maxDiskUsage = 20
    hasVacationReply = None
    vacationReplySubject = ''
    vacationReplyMessage = ''

    def __init__(self, address, spamCheckerStrength=SPAMCHECKER_STRENGTH_AVERAGE, maxDiskUsage=20, hasVacationReply='',
                 vacationReplySubject='', vacationReplyMessage=''):
        super(MailBox, self).__init__()

        self.address = address
        self.spamCheckerStrength = spamCheckerStrength
        self.maxDiskUsage = maxDiskUsage
        self.hasVacationReply = hasVacationReply
        self.vacationReplySubject = vacationReplySubject
        self.vacationReplyMessage = vacationReplyMessage

    def __eq__(self, other):
        if isinstance(other, MailBox):
            return self.address == other.address

        if hasattr(other, 'value'):
            return self.address == other.value.address

        return self.address == other


class MailForward(SudsObject):

    def __init__(self, name, targetAddress):
        super(MailForward, self).__init__()
        self.name = name
        self.targetAddress = targetAddress

    def __eq__(self, other):
        if isinstance(other, MailForward):
            return self.targetAddress == other.targetAddress and self.name == other.name

        if hasattr(other, 'value'):
            return self.targetAddress == other.value.targetAddress and self.name == other.value.name


class WebhostingService(Client):

    def __init__(self, *args, **kwargs):
        super(WebhostingService, self).__init__('WebhostingService', *args, **kwargs)

    def get_webhosting_domain_names(self):
        return self._simple_request('getWebhostingDomainNames')

    def get_available_packages(self):
        return self._simple_request('getAvailablePackages')

    def get_info(self, domain):
        """ Get available Webhosting products when available """
        return self._simple_request('getInfo', domain)

    def get_available_upgrades(self, domain):
        return self._simple_request('getAvailableUpgrades', domain)

    def create_mailbox(self, domain, mailbox):
        return self._simple_request('createMailBox', domain, mailbox, mode=MODE_RW)

    def set_mailbox_password(self, domain, mailbox, password):
        return self._simple_request('setMailBoxPassword', domain, mailbox, password, mode=MODE_RW)

    def update_mailbox(self, domain, mailbox):
        return self._simple_request('modifyMailBox', domain, mailbox, mode=MODE_RW)

    def delete_mailbox(self, domain, mailbox):
        return self._simple_request('deleteMailBox', domain, mailbox, mode=MODE_RW)

    def create_mail_forward(self, domain, mailforward):
        return self._simple_request('createMailForward', domain, mailforward, mode=MODE_RW)

    def update_mail_forward(self, domain, mailforward):
        return self._simple_request('modifyMailForward', domain, mailforward, mode=MODE_RW)

    def delete_mail_forward(self, domain, mailforward):
        return self._simple_request('deleteMailForward', domain, mailforward, mode=MODE_RW)
