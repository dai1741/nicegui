from typing import Callable, Optional

from fastapi import Request, Response

from ..dependencies import register_component
from ..events import EventArguments, UploadEventArguments, handle_event
from ..nicegui import app
from .mixins.disableable_element import DisableableElement

register_component('upload', __file__, 'upload.js')


class Upload(DisableableElement):

    def __init__(self, *,
                 multiple: bool = False,
                 max_file_size: Optional[int] = None,
                 max_total_size: Optional[int] = None,
                 max_files: Optional[int] = None,
                 on_upload: Optional[Callable] = None,
                 on_rejected: Optional[Callable] = None,
                 label: str = '',
                 auto_upload: bool = False,
                 ) -> None:
        """File Upload

        Based on Quasar's `QUploader <https://quasar.dev/vue-components/uploader>`_ component.

        :param multiple: allow uploading multiple files at once (default: `False`)
        :param max_file_size: maximum file size in bytes (default: `0`)
        :param max_total_size: maximum total size of all files in bytes (default: `0`)
        :param max_files: maximum number of files (default: `0`)
        :param on_upload: callback to execute for each uploaded file (type: nicegui.events.UploadEventArguments)
        :param on_rejected: callback to execute for each rejected file
        :param label: label for the uploader (default: `''`)
        :param auto_upload: automatically upload files when they are selected (default: `False`)
        """
        super().__init__(tag='upload')
        self._props['multiple'] = multiple
        self._props['label'] = label
        self._props['auto-upload'] = auto_upload
        self._props['url'] = f'/_nicegui/client/{self.client.id}/upload/{self.id}'

        if max_file_size is not None:
            self._props['max-file-size'] = max_file_size

        if max_total_size is not None:
            self._props['max-total-size'] = max_total_size

        if max_files is not None:
            self._props['max-files'] = max_files

        @app.post(self._props['url'])
        async def upload_route(request: Request) -> Response:
            for data in (await request.form()).values():
                args = UploadEventArguments(
                    sender=self,
                    client=self.client,
                    content=data.file,
                    name=data.filename,
                    type=data.content_type,
                )
                handle_event(on_upload, args)
            return {'upload': 'success'}

        if on_rejected:
            self.on('rejected', lambda _: handle_event(on_rejected, EventArguments(sender=self, client=self.client)),
                    args=[])

    def reset(self) -> None:
        self.run_method('reset')

    def delete(self) -> None:
        app.remove_route(self._props['url'])
        super().delete()
