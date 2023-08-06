import json
import pandas as pd
from io import StringIO
from pathlib import Path
import warnings
import pypandoc
from enum import Enum, auto
import logging


class Severity(Enum):
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class Check(object):
    def __init__(self, severity, message, check_name):
        self.message = message
        self.check_name = check_name
        self._display_severity = None
        self.display_severity = severity

    def update_value(self, new_severity):
        self.display_severity = new_severity

    @property
    def display_severity(self):
        return self._display_severity

    @display_severity.setter
    def display_severity(self, value):
        if isinstance(value, Severity):
            self._display_severity = value.name
        elif isinstance(value, str) and value in [x.name for x in Severity]:
            self._display_severity = value
        else:
            raise ValueError(f"{self.check_name} only accepts: "
                             f" {', '.join([x.name for x in Severity])}")


class CheckThresholds(Check):
    def __init__(self, thresholds, message, handler, check_name):
        self.handler = handler
        self.check_name = check_name
        self.thresholds = thresholds
        self._default_message = message
        self.message = None

    def update_severity_and_message(self, check_out):
        # using check specific handlers to set the severity and the message
        pct_fails, mssg_elements = self.handler.process_check_returns(
                                                                     check_out)
        self.message = self._default_message.format(*mssg_elements)
        self.display_severity = self.get_severity(pct_fails)

    def update_value(self, new_thresholds):
        self.thresholds = new_thresholds

    @property
    def thresholds(self):
        return self._thresholds

    @thresholds.setter
    def thresholds(self, value):
        if isinstance(value, list):
            if all((lambda x: isinstance(x, int), value))\
               and value == sorted(value):
                self._thresholds = value
            else:
                raise ValueError(f"{self.check_name} thresholds must be "
                                 "defined in ascending order, corresponding to"
                                 " the tolerances for: "
                                 f" {', '.join([x.name for x in Severity])}")
        else:
            raise TypeError(f"{self.check_name} only accepts three positive "
                            "integers in ascending order")

    def get_severity(self, value):
        if value < self.thresholds[0]:
            return Severity.WARNING
        elif value >= self.thresholds[2]:
            return Severity.CRITICAL
        else:
            return Severity.ERROR


class MissingValuesHandler(object):
    @staticmethod
    def process_check_returns(check_out):
        pct_fails = 100 * check_out[0] / check_out[1]
        message_elements = [check_out[0], pct_fails]

        return pct_fails, message_elements


class MissingValuesDataHandler(object):
    @staticmethod
    def process_check_returns(check_out):
        pct_fails = 100 * check_out[0][0] / check_out[0][1]
        message_elements = [check_out[0][0], pct_fails, check_out[1]]

        return pct_fails, message_elements


class MissingValuesSeriesHandler(object):
    @staticmethod
    def process_check_returns(check_out):
        pct_fails = 100 * check_out[0] / check_out[1]
        message_elements = [check_out[0], pct_fails]

        return pct_fails, message_elements


class OutlierValuesHandler(object):
    @staticmethod
    def process_check_returns(check_out):
        pct_fails = 100 * len(check_out[0]) / check_out[1]
        message_elements = [check_out[1], pct_fails, check_out[0]]
        return pct_fails, message_elements


class Report(object):
    # values are pandoc output formats
    valid_report_formats = {
        "html": "html",
        "md": "markdown_github",
        "pdf": "pdf",
        "docx": "docx"}
    default_report_columns_passing = [
        "original_name",
        "check_name",
        "data_origin",
        "check_pass"  # this is dropped when the report is generated

    ]
    default_report_columns_failing = [
        "original_name",
        "check_name",
        "data_origin",
        "severity",
        "issue_message",
        "check_pass"  # this is dropped when the report is generated
    ]
    default_group_by = ["original_name", "check_name"]
    default_report_file_path = Path.joinpath(Path.cwd(), "report.html")
    default_report_format = "html"
    default_report_config_file = "report-conf.json"
    column_names_map = {
        "original_name": "Parameter name",
        "data_origin": "Data origin",
        "check_name": "Type of check",
        "check_pass": "check_pass",
        "check_out": "Issue details",
        "py_name": "Python-safe parameter name (long)",
        "py_short_name": "Python-safe parameter name (long)",
        "file": "File name",
        "sheet": "Sheet name",
        "transposed": "Transposed",
        "cell": "Cell code",
        "coords": "Coordinates",
        "check_description": "Description of the check",
        "check_target": "Target of the check",
        "check_arg": "Check arguments",
        "x_row_or_coll": "Row or column number of the x axis",
        "severity": "Issue severity",
        "issue_message": "Issue description",
    }
    check_names_map = {
        "outlier_values": "Outlier detection",
        "missing_values": "Missing values",
        "missing_values_data": "Missing values in data",
        "missing_values_series": "Missing values in serie",
        "series_monotony": "Series monotony",
        "series_range": "Series range",
        "series_increment_type": "Series trend"
    }
    report_messages = {
        "PASSING_HEADER": {"html": "<h2>Passing tests</h2><br>"},
        "FAILING_HEADER": {"html": "<h1>Failing tests</h1><br>"},
        "SUMMARY_HEADER": {"html": "<h1>Summary</h1><br>"},
        "NUM_PARAMS_ANALYZED_BOLD": {
            "html": "<b>Number of model parameters analyzed</b>: {}"
        },
        "NUM_FAILING_CHECKS_BOLD": {
            "html": "<b>Number of failing checks</b>: {} ({:.2f} %)"
        },
        "NUM_CHECKS_EVALUATED_BOLD": {
            "html": "<b>Number of checks evaluated</b>: {}"},
        "NUMBER_ISSUES_PARAMETER": {
            "html": "<h2>Number of issues per parameter</h2>"},
        "NUMBER_ISSUES_PARAMETER_BY_TYPE": {
            "html":
            "<h2>Number of issues of each severity for each parameter</h2>"},
        "NUMBER_TYPE_ISSUES": {
            "html": "<h2>Number of issues of each type</h2>"},
        "NUMBER_SEVERITY_ISSUES": {
            "html": "<h2>Number of issues of each severity</h2>"},
        "NUMBER_DATA_ORIGIN": {
            "html": "<h2>Number of issues in each data file</h2>"},
        "WHITESPACE": {"html": "<br>", "md": "\n"},
    }

    default_values = {
        "outlier_values": [20, 30, 50],
        "missing_values": [20, 30, 50],
        "missing_values_data": [20, 30, 50],
        "missing_values_series": [20, 30, 50],
        "series_monotony": Severity.CRITICAL,
        "series_range": Severity.ERROR,
        "series_increment_type": Severity.ERROR}

    # the severity of the issues of these types are accompained with a
    # percentage of fails defines the handler that is needed to process the
    # thresholds
    handler_map = {
        "outlier_values": OutlierValuesHandler,
        "missing_values": MissingValuesHandler,
        "missing_values_data": MissingValuesDataHandler,
        "missing_values_series": MissingValuesSeriesHandler,
        "series_monotony": None,
        "series_range": None,
        "series_increment_type": None}

    default_check_messages = {
     "outlier_values": "The field has {} ({:.1f}%) potential outliers ({}).",
     "missing_values": "The field has {} ({:.1f}%) missing values.",
     "missing_values_data": "The field has {} ({:.1f}%) missing values "
                            "corresponding to series values: {}.",
     "missing_values_series": "The field has {} ({:.1f}%) missing series "
                              "values.",
     "series_monotony": "The series is not monotonic.",
     "series_range": "The series values are outside the given range.",
     "series_increment_type":
     "The series trend does not follow the expected trend."}

    def __init__(self, out, report_config_path, verbose):

        self.data = out
        self.verbose = verbose
        self.report_config_path = report_config_path
        self.buffer = StringIO()  # buffer to write the report to

        # Setting the default values for the report configurations. Some will
        # be overridden by the values in the report configuration file.
        self.report_path = self.__class__.default_report_file_path
        self.report_format = self.__class__.default_report_format
        self.check_objects = {}

        # load report configuration and update self.check_objects if needed
        self.update_report_config()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, out):
        df = pd.DataFrame(out)
        # adding column with the location of the data in the spreadsheet
        df["data_origin"] = df[df.columns[3:6]].apply(
            lambda x: ", ".join(x.dropna().astype(str))
            .replace("[", "")
            .replace("]", "")
            .replace("'", ""),
            axis=1,
        )
        self._data = df

    @property
    def report_config_path(self):
        return self._report_config_path

    @report_config_path.setter
    def report_config_path(self, file_path):
        """
        Checks if the file exists and is a JSON file and sets the
        report_config_file attribute.
        """
        if Path(file_path).is_file():
            if Path(file_path).suffix == ".json":
                self._report_config_path = file_path
            else:
                raise ValueError("Report configuration file must be a JSON "
                                 "file.")
        else:
            raise FileNotFoundError("Report configuration file not found.")

    def update_report_config(self):
        # load user-defined report configuration

        # generate default configuration
        self.__build_default_check_objects()

        try:
            json_dict = json.load(open(self.report_config_path,))
        except ValueError:
            raise ValueError("Report configuration file not correctly"
                             " formatted.")
        # validate the user json configuration and updates the
        # self.check_objects
        self.__validate_report_config(json_dict)

    def write_report(self, report_conf=None):

        """
        Generate the report.
        Parameters:
        -----------
        report_conf: (dict or str)
            If a dict is passed, it is used as the report configuration. If a
            str is passed, it is used as the path to the report configuration.

        Returns:
        --------
        buffer: StringIO containing the report content in html
        """

        # clean the buffer
        self.buffer.truncate(0)
        self.buffer.seek(0)

        if isinstance(report_conf, (str, Path)):
            # it's a json
            self.report_config_path = report_conf
            # load the default report configuration and update it with the new
            # json
            self.update_report_config()
        elif isinstance(report_conf, dict):
            # generate default configuration for the check objects
            self.__build_default_check_objects()
            # parse the dict
            self.__validate_report_config(report_conf)

        # we will pypandoc to convert the html to markdown
        if self.report_format in self.__class__.valid_report_formats.keys():
            format = "html"
        else:
            format = self.report_format

        # assign it again to avoid modifying the original dataframe
        # also, the write report may be called multiple times, so we need to
        # keep the original dataframe untouched
        df = self.data.copy(deep=True)
        passing = df.loc[df["check_pass"].isin([True])]
        failing = df.loc[df["check_pass"].isin([False])]
        # adds the severity and issue description columns to the failing df
        failing = self.__grade_issue_severity(failing)

        # renaming columns of the full df and of the group_by columns
        df.rename(columns=self.__class__.column_names_map, inplace=True)
        group_by = [self.__class__.column_names_map[x] for x in
                    self.__class__.default_group_by]

        # Select only the desired output columns, use clean names, and reindex
        failing = failing[
            self.__class__.default_report_columns_failing
            ].replace(
                {"check_name": self.__class__.check_names_map}
                ).rename(
                columns=self.__class__.column_names_map).set_index(group_by)

        # generate the report main body (failing checks only)
        self.__write_report_body(failing, format)

        # adding passing checks and summary tables
        if self.verbose:
            passing = passing[
                self.__class__.default_report_columns_passing
                ].replace(
                    {"check_name": self.__class__.check_names_map}
                    ).rename(
                        columns=self.__class__.column_names_map
                        ).set_index(group_by)

            self.__write_report_summary(df, passing, failing, format)

        return self.buffer

    def report_to_file(self, report):
        """
        Writes the report to a file. Uses pandoc to convert the default html
        report to the rest of supported formats.

        Parameters:
        -----------
        report: StringIO containing the report content in html

        Returns:
        --------
        None

        TODO add support for other formats available in pandoc
        """
        with open(self.report_path, "w") as f:
            if self.report_format == "html":
                f.write(report.getvalue())
            elif self.report_format == "md":
                pandoc_fmt = self.__class__.valid_report_formats[
                    self.report_format]
                output = pypandoc.convert_text(
                    report.getvalue(),
                    pandoc_fmt,
                    format="html",
                    extra_args=["--atx-headers"],
                )
                f.write(output)
            elif self.report_format == "pdf":
                output = pypandoc.convert_text(
                    report.getvalue(),
                    "pdf",
                    format="html",
                    outputfile=str(self.report_path),
                    extra_args=['--pdf-engine', 'xelatex',
                                '-V', 'geometry:landscape',
                                '-V', 'fontsize:6pt']
                )
            elif self.report_format == "docx":
                output = pypandoc.convert_text(
                    report.getvalue(),
                    "docx",
                    format="html",
                    outputfile=str(self.report_path),
                    extra_args=[]
                )

            else:
                pass

    def __build_default_check_objects(self):

        for check_name, defaults in self.__class__.default_values.items():

            if self.__class__.handler_map[check_name] is None:
                # does not need a handler
                self.check_objects[check_name] = Check(
                    defaults,
                    self.__class__.default_check_messages[check_name],
                    check_name)
            else:
                self.check_objects[check_name] = CheckThresholds(
                    defaults,
                    self.__class__.default_check_messages[check_name],
                    self.__class__.handler_map[check_name], check_name)

    def __validate_report_config(self, report_config):

        # this doesn't do anything yet
        self.__validate_report_columns(report_config)
        # this doesn't do anything yet
        self.__validate_report_column_group_by(report_config)

        self.__validate_report_format(report_config)

        self.__validate_report_path(report_config)

        self.__validate_report_item_issue_severity(report_config)

    def __validate_report_item_issue_severity(self, json_dict):
        # The default is False

        if "item_issue_severity_thresholds" not in json_dict:
            logging.info(
                "item_issue_severity_thresholds grading not defined. "
                "Using default values."
            )
        else:  # update the check_objects attribute
            for check_name, value in json_dict[
             "item_issue_severity_thresholds"].items():
                if check_name not in self.handler_map.keys():
                    raise ValueError("Invalid key in "
                                     "item_issue_severity_thresholds")
                else:
                    # updating the default values
                    self.check_objects[check_name].update_value(value)

    def __validate_report_path(self, json_dict):
        if "report_file_path" not in json_dict:
            logging.info("Using default value for report_path")

        # check if the report_path passed by the user is a valid path
        if isinstance(json_dict["report_file_path"], str):
            rep_path = Path(json_dict["report_file_path"])
            if not rep_path.suffix:
                raise ValueError(
                    "Report path must include the file name "
                    "(e.g. report.html)."
                )
            else:
                if rep_path.suffix[1:] != self.report_format:
                    raise ValueError(
                        "Report path must have the same file extension than"
                        " the defined report format."
                    )
                if not rep_path.is_absolute():
                    logging.info(
                        "Relative path provided for the report file."
                    )
                    self.report_path = rep_path.absolute()
                else:
                    self.report_path = rep_path
        else:
            raise ValueError("Report path must be a string.")

    def __validate_report_format(self, json_dict):
        if "report_format" not in json_dict:
            logging.info(
                "report_format field not present in the report "
                "configuration file. Using html as report_format"
            )
        else:
            if not isinstance(json_dict["report_format"], str):
                raise ValueError("report_format in the json file must be a "
                                 "string.")
            else:
                if (
                    json_dict["report_format"]
                    in self.__class__.valid_report_formats.keys()
                ):
                    self.report_format = json_dict["report_format"]
                else:
                    raise ValueError(
                        "The only supported report formats are {}.".format(
                            ", ".join(self.__class__.valid_report_formats.keys(
                            ))
                        )
                    )

    def __validate_report_column_group_by(self, json_dict):
        # TODO: implement the possibility that the users define how they want
        # the columns grouped by in the report
        if "group_by" in json_dict:
            warnings.warn("Not implemented yet, default grouping will be "
                          "applied.")

    def __validate_report_columns(self, json_dict):
        if "report_columns" in json_dict:
            warnings.warn("Not implemented yet, using default values for "
                          "report_columns")

    def __grade_issue_severity(self, df_fail):
        """
        Adds severity and issue_message columns to the dataframe

        """
        def issue_severity_and_description(check_out, check_object):
            if isinstance(check_object, CheckThresholds):
                check_object.update_severity_and_message(check_out)
            return pd.Series({"severity": check_object.display_severity,
                              "issue_message": check_object.message})

        new_cols = df_fail.apply(
            lambda x: issue_severity_and_description(
                x["check_out"],
                self.check_objects[x["check_name"]]
                ),
            axis=1,
        )
        df_fail = df_fail.merge(new_cols, left_index=True, right_index=True)
        return df_fail

    def __write_report_body(self, failing, format):
        """
        Writes the report body.
        """
        # Start writing the report contents in the buffer
        self.buffer.write(
            self.__class__.report_messages["FAILING_HEADER"][format])

        self.__df_to_x(failing.drop(
            labels=self.__class__.column_names_map["check_pass"],
            axis=1)
        )

        self.buffer.write(self.__class__.report_messages["WHITESPACE"][format])

    def __write_report_summary(self, df, passing, failing, format):
        """
        Writes a summary of the results.
        """
        grouped_by_param_name = (
            failing.groupby(by=self.__class__.column_names_map["original_name"]
                            )[self.__class__.column_names_map["severity"]
                              ].count().to_frame(name="Number")
        )

        grouped_by_check_type = (
            failing.groupby(by=self.__class__.column_names_map["check_name"])[
                self.__class__.column_names_map["severity"]
            ]
            .count()
            .to_frame(name="Number")
        )
        grouped_by_check_type["Percent of all issues"] = \
            100 * grouped_by_check_type["Number"] / \
            grouped_by_check_type["Number"].sum()
        grouped_by_check_type["Percent of all issues"] = \
            grouped_by_check_type["Percent of all issues"].round(decimals=1)

        grouped_by_var_name_and_severity = (
            failing.groupby([
                self.__class__.column_names_map["original_name"],
                self.__class__.column_names_map["severity"]])[
                self.__class__.column_names_map["severity"]].count(
                ).to_frame(name="Number"))

        grouped_by_severity = (
            failing.groupby(self.__class__.column_names_map["severity"])[
                self.__class__.column_names_map["severity"]].count(
                ).to_frame(name="Number"))
        grouped_by_severity["Percent of all issues"] = \
            100 * grouped_by_severity["Number"]/grouped_by_severity[
                "Number"].sum()
        grouped_by_severity["Percent of all issues"] = \
            grouped_by_severity["Percent of all issues"].round(decimals=1)

        group_by_data_origin = (
            failing.groupby(by=self.__class__.column_names_map["data_origin"])[
                self.__class__.column_names_map["severity"]
            ]
            .count()
            .to_frame(name="Number")
        )

        #######################################################################

        self.buffer.write(self.__class__.report_messages["WHITESPACE"][format])
        self.buffer.write(self.__class__.report_messages[
            "SUMMARY_HEADER"][format])

        # Lines with totals
        self.buffer.write(
            self.__class__.report_messages["NUM_PARAMS_ANALYZED_BOLD"][
                format].format(len(df[self.__class__.column_names_map[
                    "original_name"]].unique())
            )
        )
        self.buffer.write(self.__class__.report_messages["WHITESPACE"][format])
        self.buffer.write(
            self.__class__.report_messages[
                "NUM_CHECKS_EVALUATED_BOLD"][format].format(df.shape[0])
        )
        self.buffer.write(self.__class__.report_messages["WHITESPACE"][format])
        self.buffer.write(
            self.__class__.report_messages[
                "NUM_FAILING_CHECKS_BOLD"][format].format(
                failing.shape[0], 100 * failing.shape[0] / df.shape[0]
            )
        )

        # Number of issues of each severity
        self.buffer.write(self.__class__.report_messages["WHITESPACE"][format])
        self.buffer.write(self.__class__.report_messages[
            "NUMBER_SEVERITY_ISSUES"][format])
        self.__df_to_x(grouped_by_severity)

        # Number of issues of each type
        self.buffer.write(self.__class__.report_messages["WHITESPACE"][format])
        self.buffer.write(self.__class__.report_messages[
            "NUMBER_TYPE_ISSUES"][format])
        self.__df_to_x(grouped_by_check_type)

        # Number of issues in each data file
        self.buffer.write(self.__class__.report_messages["WHITESPACE"][format])
        self.buffer.write(self.__class__.report_messages[
            "NUMBER_DATA_ORIGIN"][format])
        self.__df_to_x(group_by_data_origin)

        # Number of issues of each severity for each parameter
        self.buffer.write(
            self.__class__.report_messages[
                "NUMBER_ISSUES_PARAMETER_BY_TYPE"][format]
        )
        self.__df_to_x(grouped_by_var_name_and_severity)

        # Number of issues per parameter
        self.buffer.write(self.__class__.report_messages["WHITESPACE"][format])
        self.buffer.write(
            self.__class__.report_messages["NUMBER_ISSUES_PARAMETER"][format]
        )
        self.__df_to_x(grouped_by_param_name)
        self.buffer.write(self.__class__.report_messages["WHITESPACE"][format])

        # Passing tests
        self.buffer.write(self.__class__.report_messages["WHITESPACE"][format])
        self.buffer.write(self.__class__.report_messages["PASSING_HEADER"][
                format])

        self.__df_to_x(passing.drop(
            labels=self.__class__.column_names_map["check_pass"],
            axis=1))

    def __df_to_x(self, df):
        """
        This function writes the dataframe to the buffer. It will only be
        actually useful when support for additional report formats is added.
        """

        if self.report_format in self.__class__.valid_report_formats.keys():
            df.to_html(self.buffer)
