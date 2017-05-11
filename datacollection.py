# -*- coding: utf-8 -*-
"""
Mesa Data Collection Module
===========================

DataCollector is meant to provide a simple, standard way to collect data
generated by a Mesa model. It collects three types of data: model-level data,
agent-level data, and tables.

A DataCollector is instantiated with two dictionaries of reporter names and
associated functions for each, one for model-level data and one for
agent-level data; a third dictionary provides table names and columns.

When the collect() method is called, each model-level function is called, with
the model as the argument, and the results associated with the relevant
variable. Then the agent-level functions are called on each
agent in the model scheduler.

Additionally, other objects can write directly to tables by passing in an
appropriate dictionary object for a table row.

The DataCollector then stores the data it collects in dictionaries:
    * model_vars maps each reporter to a list of its values
    * agent_vars maps each reporter to a list of lists, where each nested list
      stores (agent_id, value) pairs.
    * tables maps each table to a dictionary, with each column as a key with a
      list as its value.

Finally, DataCollector can create a pandas DataFrame from each collection.

The default DataCollector here makes several assumptions:
    * The model has a schedule object called 'schedule'
    * The schedule has an agent list called agents
    * For collecting agent-level variables, agents must have a unique_id

"""
from collections import defaultdict
import pandas as pd
from agents_creation import Policymakers, Policyentres, Externalparties
from copy import deepcopy
import copy


class DataCollector:
    """ Class for collecting data generated by a Mesa model.

    A DataCollector is instantiated with dictionaries of names of model- and
    agent-level variables to collect, associated with functions which actually
    collect them. When the collect(...) method is called, it executes these
    functions one by one and stores the results.
    
    """
    model_reporters = {}
    electorate_reporters = {}
    agent_reporters = {}
    links_reporters = {}
    team_as_reporters = {}
    team_pf_reporters = {}
    coalition_as_reporters = {}
    coalition_pf_reporters = {}

    model_vars = {}
    electorate_vars = {}
    agent_vars = {}
    links_vars = {}
    team_as_vars = {}
    team_pf_vars = {}
    coalition_as_vars = {}
    coalition_pf_vars = {}
    tables = {}

    model = None

    def __init__(self, model_reporters={}, electorate_reporters={}, agent_reporters={}, links_reporters={}, team_as_reporters={}, team_pf_reporters={}, coalition_as_reporters={}, coalition_pf_reporters={}, tables={}):
    # def __init__(self, model_reporters={}, agent_reporters_pm={}, tables={}):
        """ Instantiate a DataCollector with lists of model and agent reporters.

        Both model_reporters and agent_reporters accept a dictionary mapping a
        variable name to a method used to collect it.
        For example, if there was only one model-level reporter for number of
        agents, it might look like:
            {"agent_count": lambda m: m.schedule.get_agent_count() }
        If there was only one agent-level reporter (e.g. the agent's energy),
        it might look like this:
            {"energy": lambda a: a.energy}

        The tables arg accepts a dictionary mapping names of tables to lists of
        columns. For example, if we want to allow agents to write their age
        when they are destroyed (to keep track of lifespans), it might look
        like:
            {"Lifespan": ["unique_id", "age"]}

        Args:
            model_reporters: Dictionary of reporter names and functions.
            agent_reporters: Dictionary of reporter names and functions.

        """
        self.model_reporters = {}
        self.electorate_reporters = {}
        self.agent_reporters = {}
        self.links_reporters = {}
        self.team_as_reporters = {}
        self.team_pf_reporters = {}
        self.coalition_as_reporters = {}
        self.coalition_pf_reporters = {}

        self.model_vars = {}
        self.electorate_vars = {}
        self.agent_vars = {}
        self.links_vars = {}
        self.team_as_vars = {}
        self.team_pf_vars = {}
        self.coalition_as_vars = {}
        self.coalition_pf_vars = {}
        self.tables = {}

        for name, func in model_reporters.items():
            self._new_model_reporter(name, func)

        for name, func in electorate_reporters.items():
            self._new_electorate_reporter(name, func)

        for name, func in agent_reporters.items():
            self._new_agent_reporter(name, func)

        for name, func in links_reporters.items():
            self._new_links_reporter(name, func)

        for name, func in team_as_reporters.items():
            self._new_team_as_reporter(name, func)

        for name, func in team_pf_reporters.items():
            self._new_team_pf_reporter(name, func)

        for name, func in coalition_as_reporters.items():
            self._new_coalition_as_reporter(name, func)

        for name, func in coalition_pf_reporters.items():
            self._new_coalition_pf_reporter(name, func)

        for name, columns in tables.items():
            self._new_table(name, columns)

    def _new_model_reporter(self, reporter_name, reporter_function):
        """ Add a new model-level reporter to collect.

        Args:
            reporter_name: Name of the model-level variable to collect.
            reporter_function: Function object that returns the variable when
                               given a model instance.

        """
        self.model_reporters[reporter_name] = reporter_function
        self.model_vars[reporter_name] = []

    def _new_electorate_reporter(self, reporter_name, reporter_function):
        """ Add a new agent-level reporter to collect.

        Args:
            reporter_name: Name of the agent-level variable to collect.
            reporter_function: Function object that returns the variable when
                               given an agent object.

        """
        self.electorate_reporters[reporter_name] = reporter_function
        self.electorate_vars[reporter_name] = []

    def _new_agent_reporter(self, reporter_name, reporter_function):
        """ Add a new agent-level reporter to collect.

        Args:
            reporter_name: Name of the agent-level variable to collect.
            reporter_function: Function object that returns the variable when
                               given an agent object.

        """
        self.agent_reporters[reporter_name] = reporter_function
        self.agent_vars[reporter_name] = []

    def _new_links_reporter(self, reporter_name, reporter_function):
        """ Add a new agent-level reporter to collect.

        Args:
            reporter_name: Name of the agent-level variable to collect.
            reporter_function: Function object that returns the variable when
                               given an agent object.

        """
        self.links_reporters[reporter_name] = reporter_function
        self.links_vars[reporter_name] = []

    def _new_team_as_reporter(self, reporter_name, reporter_function):
        """ Add a new agent-level reporter to collect.

        Args:
            reporter_name: Name of the agent-level variable to collect.
            reporter_function: Function object that returns the variable when
                               given an agent object.

        """
        self.team_as_reporters[reporter_name] = reporter_function
        self.team_as_vars[reporter_name] = []

    def _new_team_pf_reporter(self, reporter_name, reporter_function):
        """ Add a new agent-level reporter to collect.

        Args:
            reporter_name: Name of the agent-level variable to collect.
            reporter_function: Function object that returns the variable when
                               given an agent object.

        """
        self.team_pf_reporters[reporter_name] = reporter_function
        self.team_pf_vars[reporter_name] = []

    def _new_coalition_as_reporter(self, reporter_name, reporter_function):
        """ Add a new agent-level reporter to collect.

        Args:
            reporter_name: Name of the agent-level variable to collect.
            reporter_function: Function object that returns the variable when
                               given an agent object.

        """
        self.coalition_as_reporters[reporter_name] = reporter_function
        self.coalition_as_vars[reporter_name] = []

    def _new_coalition_pf_reporter(self, reporter_name, reporter_function):
        """ Add a new agent-level reporter to collect.

        Args:
            reporter_name: Name of the agent-level variable to collect.
            reporter_function: Function object that returns the variable when
                               given an agent object.

        """
        self.coalition_pf_reporters[reporter_name] = reporter_function
        self.coalition_pf_vars[reporter_name] = []

    def _new_table(self, table_name, table_columns):
        """ Add a new table that objects can write to.

        Args:
            table_name: Name of the new table.
            table_columns: List of columns to add to the table.

        """
        new_table = {column: [] for column in table_columns}
        self.tables[table_name] = new_table

    def collect(self, model):
    # def collect(self, model, agent_pm):
        """ Collect all the data for the given model object. """
        if self.model_reporters:
            for var, reporter in self.model_reporters.items():
                forCopy = reporter(model)
                copied = deepcopy(forCopy)
                self.model_vars[var].append(copied)

        if self.electorate_reporters:
            for var, reporter in self.electorate_reporters.items():
                electorate_records = []
                for electorate in model.electorate_list:
                    forCopy = reporter(electorate)
                    copied = deepcopy(forCopy)
                    electorate_records.append((electorate.affiliation, copied, type(reporter(electorate))))
                self.electorate_vars[var].append(electorate_records)

        if self.agent_reporters:
            for var, reporter in self.agent_reporters.items():
                agent_records = []
                for agent in model.agent_action_list:
                    forCopy = reporter(agent)
                    copied = deepcopy(forCopy)
                    agent_records.append((agent.unique_id, copied, type(reporter(agent))))
                self.agent_vars[var].append(agent_records)

        if self.links_reporters:
            for var, reporter in self.links_reporters.items():
                links_records = []
                for links in model.link_list:
                    forCopy = reporter(links)
                    copied = copy.copy(forCopy)
                    # copied = deepcopy(forCopy)
                    links_records.append((links.unique_id, copied, type(reporter(links))))
                self.links_vars[var].append(links_records)

        if self.team_as_reporters:
            for var, reporter in self.team_as_reporters.items():
                team_as_records = []
                for team_as in model.team_list_as:
                    forCopy = reporter(team_as)
                    # copied = copy.copy(forCopy)
                    copied = deepcopy(forCopy)
                    team_as_records.append((team_as.unique_id, copied, type(reporter(team_as))))
                self.team_as_vars[var].append(team_as_records)

        if self.team_pf_reporters:
            for var, reporter in self.team_pf_reporters.items():
                team_pf_records = []
                for team_pf in model.team_list_pf:
                    forCopy = reporter(team_pf)
                    # copied = copy.copy(forCopy)
                    copied = deepcopy(forCopy)
                    team_pf_records.append((team_pf.unique_id, copied, type(reporter(team_pf))))
                self.team_pf_vars[var].append(team_pf_records)

        if self.coalition_as_reporters:
            for var, reporter in self.coalition_as_reporters.items():
                coalition_as_records = []
                for coalition_as in model.coalitions_list_as:
                    # if len(coalition_as.members) > 1:
                    forCopy = reporter(coalition_as)
                    copied = copy.copy(forCopy)
                    # copied = deepcopy(forCopy)
                    coalition_as_records.append((coalition_as.unique_id, copied, type(reporter(coalition_as))))
                self.coalition_as_vars[var].append(coalition_as_records)
                
        if self.coalition_pf_reporters:
            for var, reporter in self.coalition_pf_reporters.items():
                coalition_pf_records = []
                for coalition_pf in model.coalitions_list_pf:
                    # if len(coalition_pf.members) > 1:
                    forCopy = reporter(coalition_pf)
                    copied = copy.copy(forCopy)
                    # copied = deepcopy(forCopy)
                    coalition_pf_records.append((coalition_pf.unique_id, copied, type(reporter(coalition_pf))))
                self.coalition_pf_vars[var].append(coalition_pf_records)
                


    def add_table_row(self, table_name, row, ignore_missing=False):
        """ Add a row dictionary to a specific table.

        Args:
            table_name: Name of the table to append a row to.
            row: A dictionary of the form {column_name: value...}
            ignore_missing: If True, fill any missing columns with Nones;
                            if False, throw an error if any columns are missing

        """
        if table_name not in self.tables:
            raise Exception("Table does not exist.")

        for column in self.tables[table_name]:
            if column in row:
                self.tables[table_name][column].append(row[column])
            elif ignore_missing:
                self.tables[table_name][column].append(None)
            else:
                raise Exception("Could not insert row with missing column")

    def get_model_vars_dataframe(self):
        """ Create a pandas DataFrame from the model variables.

        The DataFrame has one column for each model variable, and the index is
        (implicitly) the model tick.

        """
        return pd.DataFrame(self.model_vars)

    def get_electorate_vars_dataframe(self):
        """ Create a pandas DataFrame from the agent variables.

        The DataFrame has one column for each variable, with two additional
        columns for tick and agent_id.

        """
        data = defaultdict(dict)
        for var, records in self.electorate_vars.items():
            for step, entries in enumerate(records):
                for entry in entries:
                    agent_id = entry[0]
                    val = entry[1]
                    data[(step, agent_id)][var] = val
        df = pd.DataFrame.from_dict(data, orient="index")
        df.index.names = ["Step", "ElectorateID"]
        return df

    def get_agent_vars_dataframe(self):
        """ Create a pandas DataFrame from the agent variables.

        The DataFrame has one column for each variable, with two additional
        columns for tick and agent_id.

        """
        data = defaultdict(dict)
        for var, records in self.agent_vars.items():
            for step, entries in enumerate(records):
                for entry in entries:
                    agent_id = entry[0]
                    val = entry[1]
                    data[(step, agent_id)][var] = val
        df = pd.DataFrame.from_dict(data, orient="index")
        df.index.names = ["Step", "AgentID"]
        return df

    def get_links_vars_dataframe(self):
        """ Create a pandas DataFrame from the agent variables.

        The DataFrame has one column for each variable, with two additional
        columns for tick and agent_id.

        """
        data = defaultdict(dict)
        for var, records in self.links_vars.items():
            for step, entries in enumerate(records):
                for entry in entries:
                    links_id = entry[0]
                    val = entry[1]
                    data[(step, links_id)][var] = val
        df = pd.DataFrame.from_dict(data, orient="index")
        df.index.names = ["Step", "LinksID"]
        return df

    def get_team_as_vars_dataframe(self):
        """ Create a pandas DataFrame from the agent variables.

        The DataFrame has one column for each variable, with two additional
        columns for tick and agent_id.

        """
        data = defaultdict(dict)
        for var, records in self.team_as_vars.items():
            for step, entries in enumerate(records):
                for entry in entries:
                    team_as_id = entry[0]
                    val = entry[1]
                    data[(step, team_as_id)][var] = val
        df = pd.DataFrame.from_dict(data, orient="index")
        df.index.names = ["Step", "TeamID_as"]
        return df

    def get_team_pf_vars_dataframe(self):
        """ Create a pandas DataFrame from the agent variables.

        The DataFrame has one column for each variable, with two additional
        columns for tick and agent_id.

        """
        data = defaultdict(dict)
        for var, records in self.team_pf_vars.items():
            for step, entries in enumerate(records):
                for entry in entries:
                    team_pf_id = entry[0]
                    val = entry[1]
                    data[(step, team_pf_id)][var] = val
        df = pd.DataFrame.from_dict(data, orient="index")
        df.index.names = ["Step", "TeamID_pf"]
        return df

    def get_coalition_as_vars_dataframe(self):
        """ Create a pandas DataFrame from the agent variables.

        The DataFrame has one column for each variable, with two additional
        columns for tick and agent_id.

        """
        data = defaultdict(dict)
        for var, records in self.coalition_as_vars.items():
            for step, entries in enumerate(records):
                for entry in entries:
                    coalition_as_id = entry[0]
                    val = entry[1]
                    data[(step, coalition_as_id)][var] = val
        df = pd.DataFrame.from_dict(data, orient="index")
        df.index.names = ["Step", "CoalitionID_as"]
        return df
    
    def get_coalition_pf_vars_dataframe(self):
        """ Create a pandas DataFrame from the agent variables.

        The DataFrame has one column for each variable, with two additional
        columns for tick and agent_id.

        """
        data = defaultdict(dict)
        for var, records in self.coalition_pf_vars.items():
            for step, entries in enumerate(records):
                for entry in entries:
                    coalition_pf_id = entry[0]
                    val = entry[1]
                    data[(step, coalition_pf_id)][var] = val
        df = pd.DataFrame.from_dict(data, orient="index")
        df.index.names = ["Step", "CoalitionID_pf"]
        return df

    def get_table_dataframe(self, table_name):
        """ Create a pandas DataFrame from a particular table.

        Args:
            table_name: The name of the table to convert.

        """
        if table_name not in self.tables:
            raise Exception("No such table.")
        return pd.DataFrame(self.tables[table_name])
