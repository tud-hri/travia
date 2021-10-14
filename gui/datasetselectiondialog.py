import os

from PyQt5 import QtWidgets

from dataobjects.enums import DataSource, HighDDatasetID, NGSimDatasetID, PNeumaDatasetID, ExiDDatasetID
from .dataset_selection_dialog_ui import Ui_DatasetSelectionDialog


class DatasetSelectionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DatasetSelectionDialog, self).__init__(parent=parent)

        self.ui = Ui_DatasetSelectionDialog()
        self.ui.setupUi(self)

        self._fill_data_source_combobox()
        self._fill_dataset_combobox()
        self.ui.dataSourceComboBox.currentIndexChanged.connect(self._fill_dataset_combobox)

        self.selected_dataset_id = None

        self.show()

    def accept(self):
        self.selected_dataset_id = self.ui.datasetComboBox.currentData()

        super().accept()

    def _fill_data_source_combobox(self):
        for data_source in DataSource:
            self.ui.dataSourceComboBox.addItem(str(data_source), userData=data_source)

    def _fill_dataset_combobox(self):
        self.ui.datasetComboBox.clear()

        current_data_source = self.ui.dataSourceComboBox.currentData()

        if current_data_source in [DataSource.HIGHD, DataSource.EXID]:

            all_ids = HighDDatasetID if current_data_source is DataSource.HIGHD else ExiDDatasetID

            for dataset_id in all_ids:
                pkl_file_path = os.path.join('data', dataset_id.data_sub_folder, dataset_id.data_file_name + '.pkl')
                csv_file_path = os.path.join('data', dataset_id.data_sub_folder, dataset_id.track_data_file_name + '.csv')

                if os.path.isfile(pkl_file_path) or os.path.isfile(csv_file_path):
                    self.ui.datasetComboBox.addItem(str(dataset_id), userData=dataset_id)
        elif current_data_source in [DataSource.NGSIM, DataSource.PNEUMA]:

            all_ids = NGSimDatasetID if current_data_source is DataSource.NGSIM else PNeumaDatasetID

            for dataset_id in all_ids:
                file_path = os.path.join('data', dataset_id.data_sub_folder, dataset_id.data_file_name)
                if os.path.isfile(file_path + '.pkl') or os.path.isfile(file_path + '.csv'):
                    self.ui.datasetComboBox.addItem(str(dataset_id), userData=dataset_id)
