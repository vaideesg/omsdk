import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
#from matplotlib import style
#from mlxtend.frequent_patterns import association_rules
import json

def dump(model_map):
    if type(model_map) == list:
        for i in model_map:
            print("{0}".format(i))
    else:
        print(json.dumps(model_map, sort_keys=True, indent=4, \
            separators=(',', ': ')))

def assoc_rules(fname):
    data2 = pd.read_csv(fname)
    comp_rindex={}
    comp_index = {}
    for index,row in data2.iterrows():
        if np.isnan(row['FQDD']):
            continue
        comp_index[row['FQDD_orig'].split('.')[0]] = int(row['FQDD'])
        comp_rindex[int(row['FQDD'])] = row['FQDD_orig'].split('.')[0]
    
    itemset = {}
    for index,row in data2.iterrows():
        if row['IPAddress'] not in itemset:
            itemset[row['IPAddress']] = []
        if row['FQDD'] in comp_rindex and \
            row['IPAddress'] in itemset and \
            row['dt_base'] not in [-999999] and \
            comp_rindex[int(row['FQDD'])] not in itemset[row['IPAddress']]:
            itemset[row['IPAddress']].append(comp_rindex[int(row['FQDD'])])
    
    vals = [i for i in itemset]
    for i in vals:
        if len(itemset[i]) == 0:
            del itemset[i]
    dataset =[]
    for i in itemset:
        dataset.append(itemset[i])
    print(dataset)
    
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=0.95, use_colnames=True)
    fis = frequent_itemsets.sort_values(by=['support'], ascending=False)
    del_entries = []

    indexes = []
    for i in fis.index:
        l = len(fis.loc[i]['itemsets'])
        if l not in indexes: indexes.append(l)
    indexes.sort()

    for i in fis.index:
        if len(fis.loc[i]['itemsets']) < indexes[(len(indexes)>>1)-1]:
            del_entries.insert(0, i)

    for i in del_entries:
        fis.drop(i, inplace=True)

    print(fis)
    #rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.7)
    #generated= rules[ (rules['confidence'] >0.999) & (rules['lift'] > 1.0) ]


def clean_data(data, func):
    del_entries = []
    for i in data.index:
        if func(data, i):
            del_entries.insert(0, i)

    for i in del_entries:
        data.drop(i, inplace=True)

def show_data(new_data, kmeans):
    new_data.insert((new_data.shape[1]), 'kmeans', kmeans)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    scatter = ax.scatter(new_data['FQDD'],
    new_data['dt_base'], c=kmeans[0], s=50)
    plt.colorbar(scatter)
    plt.show()

def clustering(fname):
    data = pd.read_csv(fname)
    data.infer_objects()
    data.fillna(0, inplace=True)
    new_data = data.drop(['IPAddress',
            'LifecycleControllerVersion',
            'FQDD_orig',
            'SystemID',
            'ComponentID',
            'DeviceID',
            'SubDeviceID',
            'VendorID',
            'SubVendorID',
            'SREC',
            'Model',
            'VersionString',
            'InstallationDate',
            'attributes',
            'HostName',
            'max_id',
            'max_id_min',
            'diff_eql_max'
            ], axis=1)
    clean_data(new_data, lambda new_data,i : new_data.loc[i]['dt_base'] in [-999999, 999999])

    model = KMeans(n_clusters=8)
    model.fit(new_data)

    clust_labels = model.predict(new_data)
    show_data(new_data, pd.DataFrame(clust_labels))

class Charting(object):
    def __init__(self, title, names, flags, show_children, components):
        self.title = title
        self.names = names
        self.flags = flags
        self.show_children = show_children
        self.components = components

    def process(self, fname):
        self._init()
        data = pd.read_csv(fname)
        data.fillna(0, inplace=True)
        ips = {}
        for i in data.index:
            if self.components and (type(data['FQDD_orig'][i]) != str):
                    continue
            comp = data['FQDD_orig'][i].split('.')[0] \
                    if self.components else data['IPAddress'][i]
            if comp not in ips:
                ips[comp] = []
                for j in range(0, len(self.names)):
                    ips[comp].append(0.0)
            self._accept(ips, data, i)

        entries = []
        for i in range(0, len(self.names)):
            entries.append([])
            for j in range(0, len(self.names)):
                entries[i].append(0.0)
    
        for i in ips:
            filtered = [j for j in range(0, len(self.names)) if ips[i][j] > 0.0]
            self._accumulate(ips[i], entries, filtered)

        #for i in ips:
        #    print("{0}->{1}".format(i, ips[i]))

        self._final(ips, entries)

    def _init(self):
        pass

    def _final(self, ips, entries):
        fig, ax = plt.subplots()
        values = [entries[i][i] for i in range(0, len(self.names))]
        cmap = plt.get_cmap("tab20")
        outer_colors = cmap(np.array([5, 6, 2, 1, 19, 8, 10]))
        cols =[5, 6, 2, 1, 19, 8, 10]
    
        size = 0.2
        ax.pie(values, labels=self.names,radius=1, colors=outer_colors,
        wedgeprops=dict(width=size, edgecolor='w'))
    
        if self.show_children:
            for i in range(1, len(self.names)):
                row_i = []
                for j in range(0, len(self.names)):
                    row_i.append(entries[j][i])
                    row_i.append(entries[j][j]-entries[j][i])
                inner_colors = cmap(np.array([cols[i],15]))
                width = 0.1
                size = 1 - 0.2 - (i-1)*width
                ax.pie(row_i, radius=size, colors=inner_colors,
                    wedgeprops=dict(width=width, edgecolor='w'))

        ax.legend(loc='upper right')
        ax.set(aspect="equal", title=self.title)
        plt.show()

    def _accept(self, ips, data, i):
        pass

    def _accumulate(self, ips, entries, filtered):
        if self.flags:
            entries[0][0] += 1
        if len(filtered):
            for idx in filtered:
                entries[filtered[0]][idx]+=(ips[idx] if self.components else 1)

    def _filter(self, data, i):
        return data['HostName'][i] in [ 'linux/esx', 'Unknown', 'win', 'bare-metal' ]


class UpdateStatusBase(Charting):
    def __init__(self, title, cost_type, names, flags=False, show_children = True, components = False):
        self.cost_type = cost_type
        self.components = components
        super().__init__(title, names, flags, show_children, components)

    def cost_it(self, data, i):
        if self.cost_type == "status":
            return data['diff_eql_max'][i]

        if data['max_id'][i] == "99.99.99":
            return 'X-Rev'
        
        from datetime import date,timedelta
        t = [int(j) for j in data['max_id_min'][i].split('.')]
        today = date.today()
        catday = today.replace(2000+t[0], t[1], t[2]+15)
        delta = today-catday
        indays = delta.days
        tt = data['attributes'][i]
        if type(tt) != str: tt = ""
        if 'Vulnerability' in tt:
            need = 30
        elif data['diff_eql_max'][i] in ['Update-After-Single-Year',
                                         'IPS/Demoted-Update']:
            need = 60
        else:
            need = 180
        # > 30 => immediate
        if indays > need:
            indays = 'Immediate'
        elif indays > 60:
            indays = 'In 180 Days'
        elif indays > 30:
            indays = 'In 60 Days'
        else:
            indays = 'In 30 Days'
        return indays

    def _accept(self, ips, data, i):
        if data['dt_base'][i] in [-999999] or (type(data['FQDD_orig'][i]) != str):
            return False
        comp = data['FQDD_orig'][i].split('.')[0] if self.components else data['IPAddress'][i]
        if self.flags:
            for iname in range(0, len(self.names)):
                if self.names[iname] in data and data[self.names[iname]][i] > 0.0:
                    ips[comp][iname] = 1
        else:
            val = ips[comp][self.names.index(self.cost_it(data, i))]
            val = val + 1 if self.components else 1
            ips[comp][self.names.index(self.cost_it(data, i))] = val

class UpdateCost(Charting):
    def __init__(self, show_children = True, cost_type="cost"):
        names = ['Cost']
        self.cost_type = cost_type
        self.costs = {
            'Disk' : 25,
            'NIC' : 10,
            'Diagnostics' : 0,
            'AHCI' : 15,
            'iDRAC' : 5,
            'ServiceModule' : 15,
            'FC' : 15,
            'CPLD' : 10,
            'DriverPack' : 0,
            'OSCollector' : 0,
            'CMC' : 15,
            'DIMM' : 15,
            'PCIeSSD' : 15,
            'USC' : 15,
            'PM' : 0,
            'NonRAID' : 15,
            'PSU' : 15,
            'BIOS' : 30,
            'Enclosure' : 15,
            'RAID' : 0,
        }
        super().__init__('Update Cost', names, False, show_children, False)

    def _init(self):
        self.ips_comps = {}

    def cost_it(self, comp, data, i):
        if self.cost_type == "cost":
            return self.costs[comp]
        return 1

    def _accept(self, ips, data, i):
        if data['dt_base'][i] in [-999999] or (type(data['FQDD_orig'][i]) != str):
            return False
        comp = data['FQDD_orig'][i].split('.')[0]
        device = data['IPAddress'][i]
        if device not in self.ips_comps:
            self.ips_comps[device] = {}
        if comp not in self.ips_comps[device]:
            ips[device][0] += self.cost_it(comp, data, i)
            self.ips_comps[device][comp] = data['diff_eql_max'][i]
            self.ips_comps[device]['_a'] = data['HostName'][i]

    def _final(self, ips, entries):
        dd = {}
        cks = []
        for i in ips:
            if ips[i][0] == 0.0: continue
            if self.ips_comps[i]['_a'] not in dd:
                dd[self.ips_comps[i]['_a']] = {}
            if self.ips_comps[i]['_a'] not in cks:
                cks.append(self.ips_comps[i]['_a'])
            dd[self.ips_comps[i]['_a']][i] = ips[i][0]
        cks.sort()
        tt = []
        for i in self.ips_comps:
            tt.append([j for j in self.ips_comps[i] \
                      if j != "_a" and self.ips_comps[i][j] != 'At-Latest'])

        fig, ax = plt.subplots()
        values = [sum(dd[i].values()) for i in cks]

        cmap = plt.get_cmap("tab20")
        outer_colors = cmap(np.array([5, 6, 2, 1, 19, 8, 10]))
        cols =[5, 6, 2, 1, 19, 8, 10]
    
        size = 0.2
        ax.pie(values, labels=cks,radius=1, colors=outer_colors,
        wedgeprops=dict(width=size, edgecolor='w'))
    
        ax.legend(loc='upper right')
        ax.set(aspect="equal", title=self.title)
        plt.show()

class UpdateStatus(UpdateStatusBase):
    def __init__(self, show_children = True, components = False):
        names = [
            'At-Latest',
            'IPS/Demoted-Update',
            'Update-After-Single-Year',
            'X-Rev',
            'Multiple-Updates-One-Applied',
            'Update-After-Multiple-Years',
            'No-Update-Found'
        ]
        super().__init__('Update Status', 'status', names, False, show_children, components)


class UpdateByWhen(UpdateStatusBase):
    def __init__(self, show_children = True, components = False):
        names = [
            'Immediate',
            'In 30 Days',
            'In 60 Days',
            'In 180 Days',
            'X-Rev'
        ]
        super().__init__('Update By When', 'bywhen', names, False, show_children, components)

class UpdateImpact(UpdateStatusBase):
    def __init__(self, show_children = True, components=False):
        names = ['', 'Vulnerability', 'Security', 'Availability',
                   'Reliability', 'Performance', ]
        super().__init__('Update Impact', 'impacts', names, True, show_children, components)

class UpdateItemsets(Charting):
    def __init__(self, show_children = True, include=['At-Latest'], exclude=[], support = 0.4):
        names = ['Cost']
        self.support = support
        self.all_s = set([
            'Update-After-Multiple-Years',
            'Update-After-Single-Year',
            'IPS/Demoted-Update',
            'At-Latest',
            'X-Rev',
            'No-Update-Found',
            'Rare-Update-One-Applied',
            'Multiple-Updates-One-Applied' ])
        if len(include) > 0 and len(exclude) > 0:
            self.include = set(include)
            self.exclude = set(exclude)
        elif len(exclude) > 0:
            self.exclude = set(exclude)
            self.include = set(self.all_s) - self.exclude
        else:
            self.include = set(include) if len(include) > 0 else self.all_s
            self.exclude = set(self.all_s) - self.include
        super().__init__('Update Itemsets', names, False, show_children, False)

    def _init(self):
        self.ips_comps = {}

    def _accept(self, ips, data, i):
        if data['dt_base'][i] in [-999999]:
            return False
        if type(data['FQDD_orig'][i]) != str:
            return False
        comp = data['FQDD_orig'][i].split('.')[0]
        device = data['IPAddress'][i]
        if device not in self.ips_comps:
            self.ips_comps[device] = {}
        if comp not in self.ips_comps[device]:
            ips[device][0] += 1
            self.ips_comps[device][comp] = data['diff_eql_max'][i]
            self.ips_comps[device]['_a'] = data['HostName'][i]
        elif (self.ips_comps[device][comp] == 'At-Latest' and
              self.ips_comps[device][comp] not in self.include):
                self.ips_comps[device][comp] = data['diff_eql_max'][i]

    def _final(self, ips, entries):
        dd = {}
        cks = []
        for i in ips:
            if ips[i][0] == 0.0: continue
            if self.ips_comps[i]['_a'] not in dd:
                dd[self.ips_comps[i]['_a']] = {}
            if self.ips_comps[i]['_a'] not in cks:
                cks.append(self.ips_comps[i]['_a'])
            dd[self.ips_comps[i]['_a']][i] = ips[i][0]
        cks.sort()
        dataset = []
        dataset2 = []
        for i in self.ips_comps:
            t = [j for j in self.ips_comps[i] if j != "_a" and \
                    self.ips_comps[i][j] in self.include and \
                    self.ips_comps[i][j] not in self.exclude]
            if len(t) != 0: dataset.append(t)

        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        frequent_itemsets = apriori(df, min_support=self.support,
                    use_colnames=True)
        fis = frequent_itemsets.sort_values(by=['support'], ascending=False)
        del_entries = []

        indexes = []
        for i in fis.index:
            l = len(fis.loc[i]['itemsets'])
            if l not in indexes: indexes.append(l)
        indexes.sort()

        for i in fis.index:
            if len(fis.loc[i]['itemsets']) < indexes[(len(indexes)>>1)-1]:
                del_entries.insert(0, i)

        for i in del_entries:
            fis.drop(i, inplace=True)

        for i in fis.index:
            print([j for j in fis.loc[i]['itemsets']])


# Update Cost:
#  How much downtime is needed
#  How should I do the downtime?

# Patterns:
# Using Installation-Date sequences

# Insights
print("---- insights ----")
#UpdateImpact().process('o.csv')
#UpdateStatus().process('o.csv')
clustering('o.csv')

print("---- decision support ----")
# Decision Making
#UpdateByWhen().process('o.csv')
#UpdateCost().process('o.csv')
#UpdateItemsets(include=['At-Latest']).process('o.csv')
#print("======")
#UpdateItemsets(exclude=['At-Latest']).process('o.csv')
#print("======")
#UpdateItemsets(include=['IPS/Demoted-Update'],support=0.1).process('o.csv')

print("---- remediation ----")
