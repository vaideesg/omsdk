#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Karthik Prabu
#
import os
import json
import logging.config
import tempfile
from enum import Enum

DEFAULT_LOGGER_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config", "logging.json")

DEFAULT_LOGGER_LOG_FILE = os.path.join(tempfile.gettempdir(), "omsdk-logs", "omsdk-logs.log")
DEFAULT_LOGGER_FORMAT = "%(asctime)s - %(levelname)-5s - %(name)s:%(lineno)d - %(message)s"
DEFAULT_LOGGER_LEVEL = logging.ERROR

logger = logging.getLogger(__name__)


# Logger Configuration Types
class LoggerConfigTypeEnum(Enum):
    BASIC = 1  # Basic Configuration
    CONFIG_FILE = 2  # Configuration File based Configuration


class LoggerConfiguration:
    @staticmethod
    def __load_config(file_type, path):
        try:
            with open(path, 'rt') as f:
                if file_type == "json":
                    config = json.load(f)
                logging.config.dictConfig(config)

        except IOError as e:
            logger.error("I/O error({0}): {1}".format(e.errno, e.strerror))

    def setup_logging(self, logger_config_type=LoggerConfigTypeEnum.BASIC,
                      logger_config_file=DEFAULT_LOGGER_CONFIG_FILE,
                      logger_log_file=DEFAULT_LOGGER_LOG_FILE,
                      logger_format=DEFAULT_LOGGER_FORMAT,
                      logger_level=DEFAULT_LOGGER_LEVEL):
        logger.info("Setting up Logging -- STARTED")

        # Basic Configuration
        if logger_config_type == LoggerConfigTypeEnum.BASIC:
            logger_log_directory = os.path.dirname(logger_log_file)

            # create log directory if doesn't exist
            if not os.path.exists(logger_log_directory):
                os.makedirs(logger_log_directory)

            # set up basic logging
            logging.basicConfig(filename=logger_log_file, format=logger_format, level=logger_level)

            # set up logging to console
            console = logging.StreamHandler()
            console.setLevel(logger_level)
            # set a format which is simpler for console use
            formatter = logging.Formatter(logger_format)
            console.setFormatter(formatter)
            logging.getLogger("").addHandler(console)

        # Logging from Configuration File
        elif logger_config_type == LoggerConfigTypeEnum.CONFIG_FILE:
            path = logger_config_file

            # Check if file exists
            if os.path.exists(path):
                file_type = path.split(os.sep)[-1].split(".")[-1].lower()

                # JSON-Based Configuration
                if file_type == "json":
                    self.__load_config(file_type, path)

                # CONF/INI-based Configuration
                elif file_type == "conf" or file_type == "ini":
                    logging.config.fileConfig(path)

                # Unsupported Configuration
                else:
                    logger.error("Unsupported configuration")
            else:
                logger.error("No Logger Configuration Specified")
        else:
            logger.error("Invalid Logger Configuration.")
        logger.info("Setting up Logging -- FINISHED")


LogManager = LoggerConfiguration()
