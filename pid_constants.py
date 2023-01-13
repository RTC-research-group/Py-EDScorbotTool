D_LEN = 22
D_Freq_Divider = 512
I_LEN = 18
I_Freq_Divider = 1260 #en el j1, diferente para los otros j
P_Spike_Expansor = 2500 # en el j1, diferente para los otros j
Encoder_Integ_LEN = 18 
Encoder_Integ_FD = 8 # en el j1, diferente para los otros j

kp = (P_Spike_Expansor + 1) * 0.00000002 * 12 # (SpikeWidth + 1) * Tclk * Vps
ki = (50000000)/(2^(I_LEN-1)*(I_Freq_Divider+1)) #Fclk/2^(nI-1)*(IGfd + 1)
kd = 50000000/(2^(D_LEN-1)*(D_Freq_Divider+1)) # Fclk/2^(nD-1)*(SDfd + 1)