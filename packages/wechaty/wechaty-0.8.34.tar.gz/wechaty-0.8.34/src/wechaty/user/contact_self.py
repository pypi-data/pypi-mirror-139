"""ContactSelf"""
from __future__ import annotations
from typing import Any, Optional, Type

from wechaty import FileBox, get_logger
from wechaty.exceptions import WechatyOperationError
from .contact import Contact

log = get_logger('ContactSelf')


class ContactSelf(Contact):
    """ContactSelf"""

    async def avatar(self, file: Optional[FileBox] = None) -> FileBox:
        """

        :param file:
        :return:
        """
        log.info('avatar(%s)' % file.name if file else '')
        if not file:
            file_box = await super().avatar(None)
            return file_box

        if self.contact_id != self.puppet.self_id():
            raise WechatyOperationError('set avatar only available for user self')

        await self.puppet.contact_avatar(self.contact_id, file)

    async def qr_code(self) -> str:
        """

        :return:
        """
        try:
            puppet_id: str = self.puppet.self_id()
        except Exception:
            raise WechatyOperationError(
                'Can not get qr_code, user might be either not logged in or already logged out')

        if self.contact_id != puppet_id:
            raise WechatyOperationError('only can get qr_code for the login user self')
        qr_code_value = await self.puppet.contact_self_qr_code()
        return qr_code_value

    @property
    def name(self) -> str:
        """
        :return:
        """
        return super().name

    async def set_name(self, name: str) -> None:
        """
        set the name of login contact
        Args:
            name: new name
        """
        await self.puppet.contact_self_name(name)
        await self.ready(force_sync=True)

    async def signature(self, signature: str) -> Any:
        """

        :param signature:
        :return:
        """
        puppet_id = self.puppet.self_id()

        if self.contact_id != puppet_id:
            raise WechatyOperationError('only can get qr_code for the login user self')

        return self.puppet.contact_signature(signature)
