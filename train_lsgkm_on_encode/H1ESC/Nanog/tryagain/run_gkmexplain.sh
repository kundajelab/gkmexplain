#!/usr/bin/env bash

~/lsgkm/bin/gkmexplain positives_test.fa lsgkm_defaultsettings_t2.model.txt gkmexplain_positives_impscores.txt

~/lsgkm/bin/gkmexplain -m 1 positives_test.fa lsgkm_defaultsettings_t2.model.txt gkmexplain_positives_hypimpscores.txt
