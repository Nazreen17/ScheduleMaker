from constants import ENABLED_OPTIMIZER_OBJECT_LIST
from COREDB.ClassPull import pull_class_object_list_via
from COREDB.MaxTemplatePrivatePull import pull_private_max_schedule_crn_2d_list
from COREDB.MaxTemplatePublicPull import pull_public_max_schedule_crn_2d_list
from COREClassStructure.TermScheduleStructure import TermSchedule

from Optimizations.DayOff import DayOff
from Optimizations.EarlyEnd import EarlyEnd
from Optimizations.InPerson import InPerson
from Optimizations.InPersonNot import Online


class OptimizerRequest:
    def __init__(self, optimizer_name=None, extra_values=None, template_id=None, user_discord_id=None,
                 max_schedule=None):
        """
        WARNING: ATTRIBUTES NOT FULLY VALIDATED ON ORIGINAL DECLARATION, USE PROPERTIES
        Used for processing all optimization requests including requests from a discord bot
        :param optimizer_name:
        :param extra_values:
        list -> Represents secondary values required by each individual optimizer
        :param template_id:
        str -> Represents if the user wants to use their personal saved template or a public template via an id
        :param user_discord_id:
        :param max_schedule:
        2D list -> CRN code based max schedule or AClass based max schedule (Occurs in multi linear optimizer processing)
        """
        self._optimizer_name = optimizer_name  # str
        self._extra_values = extra_values  # extra values
        self._template_id = template_id  # str
        self._user_discord_id = user_discord_id  # int
        self._max_schedule = max_schedule  # 2d max schedule list

    @property
    def optimizer_name(self):
        return self._optimizer_name

    @optimizer_name.setter
    def optimizer_name(self, optimizer_name):
        optimizer_name = optimizer_name.lower().replace(" ", "")

        if self.__is_valid_optimizer(optimizer_name):
            self._optimizer_name = optimizer_name
        else:
            raise ValueError(optimizer_name)

    @staticmethod
    def __is_valid_optimizer(optimizer_name):
        """
        All enabled optimizers are defined by ENABLED_OPTIMIZER_OBJECT_LIST on constants.py
        :param optimizer_name:
        :return:
        Bool -> True or False for if the optimizer name is valid/allowed
        """
        for valid_enabled_optimizer in ENABLED_OPTIMIZER_OBJECT_LIST:
            if optimizer_name == valid_enabled_optimizer.name.lower().replace(" ", ""):
                return True
        return False

    @property
    def max_schedule(self):
        return self._max_schedule

    @max_schedule.setter
    def max_schedule(self, list_of_term_schedules):
        if isinstance(list_of_term_schedules, list):
            temp = []
            for term_schedule in list_of_term_schedules:
                temp.append(term_schedule.classes)

            self._max_schedule = temp
        else:
            raise ValueError(list_of_term_schedules)

    def single_request_build_max_schedule_from_self(self):
        temp_max_schedule = self.__pull_2d_crn_max_schedule(template_id=self._template_id,
                                                            user_discord_id=self._user_discord_id)
        temp_max_schedule = self.__convert_crn_2d_to_class_obj_2d(temp_max_schedule)

        self._max_schedule = temp_max_schedule

    @staticmethod
    def __pull_2d_crn_max_schedule(template_id, user_discord_id=None):
        """
        :param template_id:
        str -> Represents if the user wants to use their personal saved template or a public template via an id
        :param user_discord_id:
        int -> Discord user id that is requesting the max schedule pull, Default = None cause public templates are valid
        :return:
        List -> A 2D crn code based max schedule list based off a template 1 or personal id
        """
        # User requests to use personal template
        if template_id == "personal" and user_discord_id is not None:  # ensure validity
            return pull_private_max_schedule_crn_2d_list(user_discord_id)
        elif template_id.isdigit():  # User requests to use public template
            return pull_public_max_schedule_crn_2d_list(template_id)
        else:
            raise ValueError

    @staticmethod
    def __convert_crn_2d_to_class_obj_2d(max_schedules):
        """
        Convert every crn code within a based 2d max schedule list into AClass type
        :param max_schedules:
        2D list -> Max Schedule Template
        :return:
        2D list -> Max Schedule Template converted to based on AClass types pulled from DB
        """
        # Pull all classes based on matching CRN codes
        all_classes = []
        found_crn_classes = []

        for schedule in max_schedules:
            for crn in schedule:
                if crn not in found_crn_classes:
                    # Store the first instance of each crn and its AClass value from pulled (indexes match)
                    found_crn_classes.append(crn)
                    all_classes += pull_class_object_list_via(crn=crn)

        # Convert/Rewrite 2D crn code based max schedule list to 2D AClass based
        for schedule_i in range(len(max_schedules)):
            for crn_i in range(len(max_schedules[schedule_i])):
                max_schedules[schedule_i][crn_i] = all_classes[
                    found_crn_classes.index(max_schedules[schedule_i][crn_i])]
                # Rewrite the 2D max schedule list from crn code based into AClass based

        return max_schedules

    @property
    def extra_values(self):
        return self._extra_values

    @extra_values.setter
    def extra_values(self, extra_values):
        self._extra_values = extra_values if extra_values is not None else []

    @property
    def template_id(self):
        return self._template_id

    @template_id.setter
    def template_id(self, template_id):
        if isinstance(template_id, str):
            template_id = template_id.replace(" ", "")
            if template_id == "personal" or template_id.isdigit():  # User requests to use public template
                self._template_id = template_id
            else:
                raise ValueError(template_id)
        elif isinstance(template_id, int):
            self._template_id = str(template_id)

    @property
    def user_discord_id(self):
        return self._user_discord_id

    @user_discord_id.setter
    def user_discord_id(self, user_discord_id):
        self._user_discord_id = user_discord_id

    def build_request(self):
        """
        :return:
        DualShiftOptimizerStructure subclass -> Return a complete optimizer
        """
        # ALSO UPDATE: constants.py -> ENABLED_OPTIMIZER_OBJECT_LIST

        if self._optimizer_name == EarlyEnd().name.lower():
            return EarlyEnd(schedule_list=self._max_schedule)
        elif self._optimizer_name == DayOff().name.lower():
            return DayOff(schedule_list=self._max_schedule, day_off=self.extra_values[0])
        elif self._optimizer_name == InPerson().name.lower():
            return InPerson(schedule_list=self._max_schedule)
        elif self._optimizer_name == Online().name.lower():
            return Online(schedule_list=self._max_schedule)
        else:
            raise ValueError

    def __str__(self):
        return (f"--- OptimizerRequest Object ---\n"
                f"optimizer_name = {self._optimizer_name}\n"
                f"extra_values = {self._extra_values}\n"
                f"template_id = {self._template_id}\n"
                f"user_discord_id = {self._user_discord_id}\n"
                f"max_schedule = {self._max_schedule}")
