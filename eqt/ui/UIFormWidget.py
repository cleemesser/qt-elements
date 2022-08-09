from qtpy import QtWidgets
from qtpy.QtCore import Qt


class UIFormWidget(object):
    """
             QWidget or QDockWidget
    +----------------------------------------------------------+
    |        QVBoxLayout                                       |
    |   +---------------------------------------------------+  |
    |   |    QGroupBox                                      |  |
    |   |                                                   |  |
    |   |    +------------------------------------------+   |  |
    |   |    |   QFormLayout                            |   |  |
    |   |    |                                          |   |  |
    |   |    |                                          |   |  |
    |   |    +------------------------------------------+   |  |
    |   |                                                   |  |
    |   +---------------------------------------------------+  |
    |                                                          |
    +----------------------------------------------------------+
    """

    def createForm(self):
        # Add vertical layout to dock contents
        verticalLayout = QtWidgets.QVBoxLayout(self)
        verticalLayout.setContentsMargins(10, 10, 10, 10)

        # Add vertical layout to main widget (self)
        # verticalLayout.addWidget(self)
        self.setLayout(verticalLayout)

        # Add group box
        groupBox = QtWidgets.QGroupBox(self)

        # Add form layout to group box
        groupBoxFormLayout = QtWidgets.QFormLayout(groupBox)

        # Add elements to layout
        verticalLayout.addWidget(groupBox)

        self.num_widgets = 0
        self.uiElements = {
            "verticalLayout": verticalLayout,
            "groupBox": groupBox,
            "groupBoxFormLayout": groupBoxFormLayout,
        }
        self.widgets = {}

    @property
    def groupBox(self):
        return self.uiElements["groupBox"]

    def addSpanningWidget(self, qwidget, name):
        self._addWidget(name, qwidget)

    def addWidget(self, qwidget, qlabel, name):
        self._addWidget(name, qwidget, qlabel)

    def addTitle(self, qlabel, name):
        if isinstance(qlabel, str):
            txt = qlabel
            qlabel = QtWidgets.QLabel(self.uiElements["groupBox"])
            qlabel.setText(txt)
        qlabel.setStyleSheet("font-weight: bold")
        self._addWidget(name, qlabel)

    def addSeparator(self, name):
        # Adds horizontal separator to the form
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.HLine)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self._addWidget(name, frame)

    def _addWidget(self, name, qwidget, qlabel=None):
        formLayout = self.uiElements["groupBoxFormLayout"]

        # Create the widgets:

        widgetno = self.num_widgets

        # add the field
        field = "{}_field".format(name)
        self.widgets[field] = qwidget

        if qlabel is not None:
            # add the label
            label = "{}_label".format(name)
            if isinstance(qlabel, str):
                txt = qlabel
                qlabel = QtWidgets.QLabel(self.uiElements["groupBox"])
                qlabel.setText(txt)
            formLayout.setWidget(widgetno, QtWidgets.QFormLayout.LabelRole, qlabel)

            # save a reference to label widgets in the dictionary
            self.widgets[label] = qlabel

            field_form_role = QtWidgets.QFormLayout.FieldRole

        else:
            # In the case we don't have a qlabel, set a spanning widget:
            field_form_role = QtWidgets.QFormLayout.SpanningRole

        formLayout.setWidget(widgetno, field_form_role, qwidget)
        self.num_widgets += 1


class FormWidget(QtWidgets.QWidget, UIFormWidget):
    def __init__(self, parent=None):
        # dockWidgetContents = QtWidgets.QWidget()

        QtWidgets.QWidget.__init__(self, parent)
        self.createForm()


class FormWidgetState(FormWidget):
    """clm: add code to make it easy to extract the state from the form
    just supports QCheckBox and QLineEdit fields so far in the form

    TODO
    other potential forms: QComboBox, QCalendarWidget, QDateEdit, QTimeEdit
    QSpinBox, QDail, ?QDirModel, QDoubleSpinBox
    ?QRadioButton, ?Toggle button,
    QSlider, ?QtextBrowser, QTreeWidget
    """

    def get_state(self):
        "return state as a dictionary"
        # find the fields in the form
        fields = {
            ii: self.widgets[ii] for ii in self.widgets if str(ii).endswith("_field")
        }
        state = {}
        fieldlen = len("_field")
        for kk, vv in fields.items():
            # print(f"{kk=}", end=" ")
            # print(f"{type(vv)=}", end=" ")
            # print(f"{vv.__class__.__name__=}")

            key = kk[:-fieldlen]  # strip off "_field" ending
            if vv.__class__.__name__ in ["QCheckBox"]:
                # print(f"{vv.checkState()}", end=" ")
                state[key] = True if vv.checkState() == Qt.CheckState.Checked else False
                # print(f"{True if vv.checkState() == Qt.CheckState.Checked else False}")
            # widgets with state as text
            if vv.__class__.__name__ in ["QLineEdit"]:
                # print(f"{vv.text()=}")
                state[key] = vv.text()

        # other potential forms: QComboBox, QCalendarWidget, QDateEdit, QTimeEdit
        # QSpinBox, QDail, ?QDirModel, QDoubleSpinBox
        # ?QRadioButton, ?Toggle button,
        # QSlider, ?QtextBrowser, QTreeWidget
        return state

    def reset_form(self):
        fields = {
            ii: self.widgets[ii] for ii in self.widgets if str(ii).endswith("_field")
        }
        for kk, ww in fields.items():

            if ww.__class__.__name__ in ["QCheckBox"]:
                # ww.setCheckState(Qt.CheckState.UnChecked)
                ww.setChecked(False)
                # print(f"try to reset {ww}")
            if ww.__class__.__name__ in ["QLineEdit"]:
                ww.setText("")  # clear text


class FormDockWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None, title=None):
        QtWidgets.QDockWidget.__init__(self, parent)
        widget = FormWidget(parent)
        self.setWidget(widget)
        if title is not None:
            self.setObjectName(title)

    def addWidget(self, qwidget, qlabel, name):
        self.widget().addWidget(qwidget, qlabel, name)


class UIFormFactory(QtWidgets.QWidget):
    # def generateUIFormView(QtWidgets.QWidget):
    """creates a widget with a form layout group to add things to

    basically you can add widget to the returned groupBoxFormLayout and paramsGroupBox
    The returned dockWidget must be added with
    main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockWidget)
    """

    @staticmethod
    def getQDockWidget(parent=None):
        return FormDockWidget(parent)

    @staticmethod
    def getQWidget(parent=None):
        return FormWidget(parent)
