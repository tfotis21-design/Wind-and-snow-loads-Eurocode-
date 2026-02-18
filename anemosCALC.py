import math
import anemosData  # Το αρχείο με τους πίνακες που έχετε ανεβάσει
ro = 1.25

def calculate_vb(vb0, c_dir, c_season):
    vb = vb0 * c_dir * c_season
    return vb

def calculate_kr(z0):
    kr = 0.19 * ((z0/0.05)**0.07)
    return kr

def calculate_cr(kr, z, z0 , zmin):
    if z <= 200 and z >= zmin :
        cr= kr * math.log( z / z0)
    else :
        cr = kr * math.log(zmin / z0)
    return cr


def calculate_vm(cr,c0,vb):
    vm = cr * c0 * vb
    return vm

def calculate_In(z,zmin, z0, c0):
    if z <= 200 and z >= zmin :
        In =  1 / (c0 * math.log(z/z0))
    else :
        In =  1 / (c0 * math.log(zmin/z0))
    return In


def calculate_qp(In,ro,vm):
    qp= (1 + (7 * In)) *(0.5 * ro * (vm**2))
    return qp /1000

def calculate_Aref_mono(d,b,a):
    Aref = ( (d *b) / (math.cos(a)))
    return Aref

def calculate_Aref_duo(d,b,a):
    Aref = (( (d/2) *b) / (math.cos(a)))
    return Aref

def calculate_F(qp, maxcf, mincf, Aref ):
    f_max = qp * maxcf * Aref
    f_min = qp * mincf * Aref
    return f_max , f_min

def angle_data(table, alpha):
    keys = sorted([k for k in table.keys() if isinstance(k, (int, float))])
    if alpha in keys:
        return table[alpha], True
    if alpha < keys[0]: return table[keys[0]], False
    if alpha > keys[-1]: return table[keys[-1]], False
    low_key = None
    high_key = None
    for k in keys:
        if k < alpha:
            low_key = k
        elif k > alpha:
            high_key = k
            break
    w = (alpha - low_key) / (high_key - low_key)
    data_low = table[low_key]  # π.χ. για 5 μοίρες
    data_high = table[high_key]  # π.χ. για 10 μοίρες
    final_data = {}
    for cat in data_low:  # cat είναι 'total', 0 ή 1


        if isinstance(data_low[cat], dict):
            final_data[cat] = {}  # Φτιάχνουμε νέο άδειο λεξικό για την κατηγορία

            dict_low = data_low[cat]
            dict_high = data_high[cat]



            # Α. Παρεμβολή για το Cf (Ξεχωριστά)
            if "Cf" in dict_low:
                cf1 = dict_low["Cf"]
                cf2 = dict_high["Cf"]
                cf_new = cf1 + (cf2 - cf1) * w
                final_data[cat]["Cf"] = cf_new

            # Β. Παρεμβολή για τις Ζώνες (Cp,net) (Ξεχωριστά)
            for key in dict_low:
                if key != "Cf":  # Αν δεν είναι το Cf, είναι ζώνη (A, B, C...)
                    val1 = dict_low[key]
                    val2 = dict_high[key]
                    val_new = val1 + (val2 - val1) * w
                    final_data[cat][key] = val_new

    return final_data, True






