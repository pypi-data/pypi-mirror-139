from scipy.signal import butter, lfilter_zi, filtfilt  # , freqz
import numpy as np
from mne.io import read_raw_edf
from mne.decoding import CSP
import matplotlib.pyplot as plt
import logging
import seaborn as sns
import mne
from numpy import matlib
from sklearn.base import BaseEstimator, TransformerMixin

# %%


def leer_bci42a_train_full(path_filename, clases, Ch, vt):

    raw = read_raw_edf(path_filename, preload=False)
    sfreq = raw.info['sfreq']

    # raw.save('tempraw.fif',overwrite=True)#, tmin=3, tmax=5,overwrite = True)
    # rawo = mne.io.read_raw_fif('tempraw.fif', preload=True)  # load data
    # depurar canales
    # rawo.plot()

    # clases_b = [769,770,771,772] #codigo clases
    # Indices de las actividades.
    i_muestras_ = raw._raw_extras[0]['events'][1]
    # Marcadores de las actividades.
    i_clases_ = raw._raw_extras[0]['events'][2]

    remov = np.ndarray.tolist(i_clases_)                 # Quitar artefactos.
    # Elimina los trials con artefactos.
    Trials_eli = 1023
    # Identifica en donde se encuentra los artefactos.
    m = np.array([i for i, x in enumerate(remov) if x == Trials_eli])
    m_ = m + 1
    tt = np.array(raw._raw_extras[0]['events'][0] * [1], dtype=bool)
    tt[m] = False
    tt[m_] = False
    # indices en muestra del inicio estimulo -> tomar 2 seg antes y 5 seg despues
    i_muestras = i_muestras_[tt]
    i_clases = i_clases_[tt]  # tipo de clase

    # i_muestras = i_muestras_ # indices en muestra del inicio estimulo -> tomar 2 seg antes y 5 seg despues
    # i_clases = i_clases_ # tipo de clase

    #eli = 1023
    #ind = i_clases_ != eli
    #i_clases = i_clases_[ind]
    #i_muestras = i_muestras_[ind]
    ni = np.zeros(len(clases))
    for i in range(len(clases)):
        ni[i] = np.sum(i_clases == clases[i])  # izquierda

    Xraw = np.zeros((int(np.sum(ni)), len(Ch), int(sfreq * (vt[1] + vt[0]))))
    y = np.zeros(int(np.sum(ni)))
    ii = 0
    for i in range(len(clases)):
        for j in range(len(i_clases)):
            if i_clases[j] == clases[i]:
                rc = raw[:, int(i_muestras[j] - vt[0] * sfreq)                         :int(i_muestras[j] + vt[1] * sfreq)][0]
                rc = rc - np.mean(rc)
                Xraw[ii, :, :] = rc[Ch, :]
                y[ii] = int(i + 1)
                ii += 1

    return i_muestras, i_clases, raw, Xraw, y, ni, m

# %%


def leer_bci42a_test_full(path_filename, clases, Ch, vt):

    raw = read_raw_edf(path_filename, preload=False)
    sfreq = raw.info['sfreq']

    # raw.save('tempraw.fif',overwrite=True)#, tmin=3, tmax=5,overwrite = True)
    # rawo = mne.io.read_raw_fif('tempraw.fif', preload=True)  # load data
    # depurar canales
    # rawo.plot()

    # clases_b = [769,770,771,772] #codigo clases
    # Indices de las actividades.
    i_muestras_ = raw._raw_extras[0]['events'][1]
    # Marcadores de las actividades.
    i_clases_ = raw._raw_extras[0]['events'][2]

    # remov   = np.ndarray.tolist(i_clases_)                 # Quitar artefactos.
#    Trials_eli = 1023                                   # Elimina los trials con artefactos.
#    m       = np.array([i for i,x in enumerate(remov) if x==Trials_eli])   # Identifica en donde se encuentra los artefactos.
#    m_      = m+1
#    tt      = np.array(raw._raw_extras[0]['events'][0]*[1],dtype=bool)
#    tt[m]   = False
#    tt[m_]  = False
#    i_muestras = i_muestras_[tt] # indices en muestra del inicio estimulo -> tomar 2 seg antes y 5 seg despues
#    i_clases = i_clases_[tt] # tipo de clase
#
    # indices en muestra del inicio estimulo -> tomar 2 seg antes y 5 seg despues
    i_muestras = i_muestras_
    i_clases = i_clases_  # tipo de clase

    ni = np.zeros(len(clases))
    for i in range(len(clases)):
        ni[i] = np.sum(i_clases == clases[i])  # izquierda

    Xraw = np.zeros((int(np.sum(ni)), len(Ch), int(sfreq * (vt[1] + vt[0]))))
    #y = np.zeros(int(np.sum(ni)))
    ii = 0
    for i in range(len(clases)):
        for j in range(len(i_clases)):
            if i_clases[j] == clases[i]:
                rc = raw[:, int(i_muestras[j] - vt[0] * sfreq)                         :int(i_muestras[j] + vt[1] * sfreq)][0]
                rc = rc - np.mean(rc)
                Xraw[ii, :, :] = rc[Ch, :]
                #y[ii] = int(clases[i])
                ii += 1

    return i_muestras, i_clases, raw, Xraw

# %% Filters


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)  # lfilter(b, a, data)
    return y

# %% Bank filter


def bank_filter_epochsEEG(Xraw, fs, f_frec):  # Xraw[nepochs,nchannels]
    nf, ff = f_frec.shape
    epochs, channels, T = Xraw.shape
    Xraw_f = np.zeros((epochs, channels, T, nf))
    for f in range(nf):
        lfc = f_frec[f, 0]
        hfc = f_frec[f, 1]
        b, a = butter_bandpass(lfc, hfc, fs)
        zi = lfilter_zi(b, a)
        Xraw_f[:, :, :, f] = filtfilt(b, a, Xraw, axis=2)
        # for n in range(epochs):
        #    for c in range(channels):
                # print(c)
        #        zi = lfilter_zi(b, a)
        #        Xraw_f[n,c,:,f] = lfilter(b, a, Xraw[n,c,:],zi = zi*Xraw[n,c,0])[0]
                #Xraw_f[n,c,:,f] = lfilter(b, a, Xraw[n,c,:])
    return Xraw_f

# %% CSP epochs


def CSP_epochsEEG(Xraw, y, ncomp):  # Xraw[nepochs,nchannels]

    csp = CSP(n_components=ncomp, reg='empirical',
              log=True, norm_trace=False)
    epochs, channels, T, nf = Xraw.shape
    Xcsp = np.zeros((epochs, ncomp, nf))
    csp_l = []
    for f in range(nf):

        csp_l.append(csp.fit(Xraw[:, :, :, f], y))
        Xcsp[:, :, f] = csp_l[f].transform(Xraw[:, :, :, f])

    return csp_l, Xcsp


# %% CSP custom sklearn


class CSP_epochs_filter_extractor(TransformerMixin, BaseEstimator):
    def __init__(self):
        logging.warning(
            "Deprecated!!, please use 'CSP_epochs_filter_extractor' instead of 'CSPEpochsFilterExtractor'")


class CSPEpochsFilterExtractor(TransformerMixin, BaseEstimator):
    def __init__(self, fs, f_frec=[4, 30], ncomp=4, reg='empirical'):
        self.reg = reg
        self.fs = fs
        self.f_frec = f_frec
        self.ncomp = ncomp

    def _averagingEEG(self, X):

        epochs, channels, T = X.shape
        Xc = np.zeros((epochs, channels, T))
        for i in range(epochs):
            Xc[i, :, :] = X[i, :, :] - np.mean(X[i, :, :])
        return Xc

    def _bank_filter_epochsEEG(self, X):
        nf, ff = self.f_frec.shape
        epochs, channels, T = X.shape
        X_f = np.zeros((epochs, channels, T, nf))
        for f in range(nf):
            lfc = self.f_frec[f, 0]
            hfc = self.f_frec[f, 1]
            b, a = butter_bandpass(lfc, hfc, self.fs)
            X_f[:, :, :, f] = filtfilt(b, a, X, axis=2)
        return X_f

    def _CSP_epochsEEG(self, Xraw, y, *_):
        ncomp = self.ncomp
        mne.set_log_level('WARNING')
        epochs, channels, T, nf = Xraw.shape
        Xcsp = np.zeros((epochs, self.ncomp, nf))
        csp_l = []
        for f in range(nf):
            csp_l += [CSP(n_components=ncomp, reg=self.reg, log=True,
                          transform_into='average_power').fit(Xraw[:, :, :, f], y)]
            Xcsp[:, :, f] = csp_l[f].transform(Xraw[:, :, :, f])
        return csp_l, Xcsp

    def fit(self, Xraw, y, *_):
        Xraw = self._averagingEEG(Xraw)
        Xraw_f = self._bank_filter_epochsEEG(Xraw)
        self.csp_l, self.Xcsp = self._CSP_epochsEEG(Xraw_f, y)
        return self

    def transform(self, Xraw, *_):
        Xraw = self._averagingEEG(Xraw)
        Xraw_f = self._bank_filter_epochsEEG(Xraw)
        epochs, channels, T, nf = Xraw_f.shape
        ncomp = self.ncomp
        result = np.zeros((epochs, ncomp, nf))
        for f in range(nf):
            result[:, :, f] = self.csp_l[f].transform(Xraw_f[:, :, :, f])
        result = result.reshape(np.size(result, 0), -1)
        return result


def eeg_nor(Xraw, sca=1e5):  # Xraw[epochs,ch,T]
    epochs, chs, T = Xraw.shape
    Xrawp = np.zeros((epochs, chs, T))
    for ep in range(epochs):
        for c in range(chs):
            Xrawp[ep, :, :] = sca * \
                (Xraw[ep, :, :] - Xraw[ep, :, :].mean(axis=0))
    return Xrawp


# data[channels, samples]
def plot_eeg(data, sample_rate, channels_names, sca=0.75):
    #  Como se conoce la frecuencia de muestreo es posible recuperar el vector del tiempo
    time = np.linspace(0, data.shape[1] / sample_rate, data.shape[1])

    fig = plt.gcf()  # plt.figure(figsize=(16, 9), dpi=90)
    sumf = sca * \
        np.max(
            sca * (data - matlib.repmat(data.mean(axis=1).reshape(-1, 1), 1, data.shape[1])))
     # Se reemplazan los valores numéricos del eje Y por los nombres de los canales
    plt.yticks(np.arange(0, sumf * len(channels_names), sumf), channels_names)

    color = sns.color_palette('husl', n_colors=data.shape[0])
    # Como los datos están en vertical (columnas) se reorientan con la transpuesta para poder visualizar los canales
    for i in range(data.shape[0]):  # se ignora la última columna
        # Para que no queden los canales sobrepuestos, antes de graficar se centra y se le suma un entero para desplazarlo ligeramente hacia arriba.
        plt.plot(time, (data[i, :] - data[i, :].mean()
                        ) + sumf * i, color=color[i])
    return


def plot_confusion_matrix_MS(cm_m, cm_s, classes,
                             normalize=False,
                             title=None,
                             cmap=plt.cm.Blues):

    fig, ax = plt.subplots()
    im = ax.imshow(cm_m, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm_m.shape[1]),
           yticks=np.arange(cm_m.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.1f' if normalize else 'd'
    thresh = cm_m.max() / 2.
    for i in range(cm_m.shape[0]):
        for j in range(cm_m.shape[1]):
            s = format(cm_m[i, j], '.1f') + "$\pm$" + \
                format(cm_s[i, j], '.1f')
            ax.text(j, i, s, ha="center", va="center",
                    color="white" if cm_m[i, j] > thresh else "black", fontsize=12)
    fig.tight_layout()
    return ax
# %%

