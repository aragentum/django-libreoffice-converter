import os
import re
import signal
import sys
import logging
import subprocess

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from web.api.exceptions import LibreOfficeError
from web.api.utils import Service


class LibreOfficeConverterService(Service):
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        super().__init__()
        if settings.CONVERTER_TEMP_FILES_FOLDER:
            self.TEMP_FILES_FOLDER = settings.CONVERTER_TEMP_FILES_FOLDER
            os.makedirs(self.TEMP_FILES_FOLDER, exist_ok=True)

            self.TEMP_PROFILES_FOLDER = os.path.join(self.TEMP_FILES_FOLDER, 'profiles')
            os.makedirs(self.TEMP_PROFILES_FOLDER, exist_ok=True)
        else:
            raise ImproperlyConfigured("Unset the CONVERTER_TEMP_FILES_FOLDER setting variable")

    def convert_to_pdf(self, input_file_path) -> str:
        return self._convert_to(input_file_path=input_file_path, converter='pdf')

    def _convert_to(self, input_file_path: str, converter: str):
        self.logger.debug("Converting file to %s: %s", converter, input_file_path)
        process_stdout = self._run_libreoffice_subprocess(input_file_path, converter)
        return self._parse_subprocess_stdout(process_stdout)

    def _parse_subprocess_stdout(self, process_stdout: bytes):
        match_output = re.search('-> (.*?) using filter', process_stdout.decode() if process_stdout else '')
        output_file_path = match_output.group(1) if match_output else None

        if output_file_path and os.path.isfile(output_file_path):
            return output_file_path
        else:
            self.logger.error("Can't find converted file. Output: %s", process_stdout)
            raise LibreOfficeError("Unknown conversion error.")

    def _run_libreoffice_subprocess(self, input_file_path: str, converter: str) -> bytes:
        lo_profile_path = os.path.join(self.TEMP_PROFILES_FOLDER, f"lo_p_{os.getpid()}")
        if sys.platform == 'win32':
            lo_profile_path = f'/{lo_profile_path}'
        args = [settings.LIBREOFFICE_PATH,
                f"-env:UserInstallation=file://{lo_profile_path}",
                '--headless', '--norestore',
                '--convert-to', converter,
                '--outdir', self.TEMP_FILES_FOLDER,
                input_file_path]

        if sys.platform == 'win32':
            process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                       creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        else:
            process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                       preexec_fn=os.setsid)
        try:
            process_stdout, _ = process.communicate(timeout=settings.CONVERTER_TIMEOUT_PROCESS)
        except subprocess.TimeoutExpired:
            self.logger.error('Timeout subprocess for file {}'.format(input_file_path))
            if sys.platform == 'win32':
                process.send_signal(signal.CTRL_BREAK_EVENT)
                process.kill()
            else:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            raise LibreOfficeError("Timeout converting process.")

        return process_stdout


libreoffice_converter_service = LibreOfficeConverterService()
