import random
import uuid
import re


class UuidTools:
    """
    Tools to update uuid consistently, maybe this should not be a class but a module...
    """

    def __init__(self, salt='', seed=None):
        # maybe salt should be in the function instead... but maybe is ok to keep consistency
        self.salt = salt
        self.seed = seed
        self.Uuid_string = r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
        self.regex_pat = re.compile(self.Uuid_string, flags=re.IGNORECASE)

    def replace_id(self, seed):
        """
        generates new from another uuid adds a seed and a salt to avoid collisions,
        """
        if seed:
            rd = random.Random()
            # when coping a config two times we need to put salt
            seed = seed + self.salt
            rd.seed(seed)
            return str(uuid.UUID(int=rd.getrandbits(128), version=4)).upper()

    def get_uuid(self, number: int = 1):
        """
        generates new ids,
        """
        if self.seed:
            print(f"Generated with seed: {self.seed}")
            rd = random.Random()
            rd.seed(self.seed)
            return [str(uuid.UUID(int=rd.getrandbits(128), version=4)).upper() for i in range(number)]
        else:
            return [str(uuid.uuid4()).upper() for i in range(number)]

    def consistent_id_change(self, series, order=1):
        """
        Changes an id to another one where the same input will give always same output
        Need to apply this in some places
        Uuid tools
        """
        if isinstance(series, str):
            series = self.replace_id(series)
        else:
            series = series.apply(self.replace_id)

        while order > 1:
            order -= 1
            series = self.consistent_id_change(series)
        return series

    def permute_id_by_dict(self, series, replace_dictionary):
        """Permute uuid given a dictionary"""
        # series = series.copy()
        # for word, initial in replace_dictionary.items(): # todo support string
        #    string = string.replace(word, initial)
        return series.str.replace(self.regex_pat, lambda x: replace_dictionary[x[0]], regex=True)

    def permute_in_text_rows(self, series):
        """Permute when uuid are somewhere in a string """
        # series = series.copy()
        return series.str.replace(self.regex_pat, lambda x: self.replace_id(x[0]), regex=True)

    def make_uuid_upper(self, series):
        return series.str.replace(self.regex_pat, lambda x: x[0].upper(), regex=True)

    def apply_to_regex_uuid(self, series, fun):  # delete?
        return series.str.replace(self.regex_pat, lambda x: fun(x[0]), regex=True)

    def permute_id_for_keys(self, df, keys_to_permute, row_keys_to_permute, inplace=True):
        """
        Permute Ids in a table keys to permute are clean keys, row_keys when the ids are in
        a calculation or in a text for example
        """
        if inplace:
            table = df
        else:
            table = df.copy()

        keys_to_permute = table.keys()[table.keys().isin(keys_to_permute)]
        row_keys_to_permute = table.keys()[table.keys().isin(row_keys_to_permute)]
        for key in keys_to_permute:
            table.loc[table.index, key] = self.consistent_id_change(table[key])
        for key in row_keys_to_permute:
            table.loc[table.index, key] = self.permute_in_text_rows(table[key])
        return table

    @staticmethod
    def format_uuid(uuid_str):
        """Given a hex number with the proper size transforms it in a uuid"""
        return f"{uuid_str[:8]}-{uuid_str[8:12]}-{uuid_str[12:16]}-{uuid_str[16:20]}-{uuid_str[20:]}".upper()

    @staticmethod
    def join_uuid(uuid_string):
        return ''.join(uuid_string.split('-'))

    def get_uuid_set(self, series):
        """
        Gets a series of uuid sets contained in a series
        # todo: support string  def get_uuid_set(string) return set(re.findall(regex_pat, string))
        """
        series = series.copy()
        uuid_sets = series.str.extractall(self.regex_pat)
        uuid_sets.columns = ['key']
        uuid_sets = uuid_sets.groupby(level=0)['key'].apply(set)
        series.loc[:] = None
        series.loc[uuid_sets.index] = uuid_sets
        return series

    def get_set_of_sets(self, series):
        series = self.get_uuid_set(series)
        return set().union(*series)  # set.union(*bla)

    def fill_ids(self, df_in, key='ID'):
        df = df_in.copy()
        df.loc[df.ID.isna(), key] = self.get_uuid(len(df[df.ID.isna()]))
        return df


# feistel inspired algorithm ########################################
# ON DEV  for generation cyclic permutation secure ID #################

def join_uuid(uuid_string):
    return ''.join(uuid_string.split('-'))


def resize_bin(bin_string, size):
    return "0" * (size - len(bin_string)) + bin_string


def hex_to_bin(hex_string, size=128):
    bin_string = bin(int(hex_string, 16))[2:]
    return resize_bin(bin_string, size)


def bin_to_hex(bin_string):
    return hex(int(bin_string, 2))[2:].upper()


def xor_string(array_a, array_b):
    # len(A)==len(B)
    bin_string = int(array_a, 2) ^ int(array_b, 2)
    bin_string = bin(bin_string)[2:]
    return resize_bin(bin_string, len(array_a))


def spilt_in_half(bin_string, size=128):
    return bin_string[0:size // 2], bin_string[size // 2:]


def formatuuid(uuid):
    """
    Given a hex number with the proper size transforms it in a uuid
    """
    return (uuid[:8] + '-' + uuid[8:12] + '-' + uuid[12:16] + '-' + uuid[16:20] + '-' + uuid[20:]).upper()


def reverse_uuid(uuid, key):
    reversal = hex_to_bin(join_uuid(key))  # maybe not necessary
    reversal = reversal[64:] + reversal[0:64]
    return formatuuid(bin_to_hex(reversal))


# https://en.wikipedia.org/wiki/Feistel_cipher
def encryption(_uuid, key):
    """
    Feistel cipher based encryption
    """
    K1, K2 = spilt_in_half(hex_to_bin(join_uuid(key)))
    L1, R1 = spilt_in_half(hex_to_bin(join_uuid(_uuid)))

    # first round of Feistel
    f1 = xor_string(R1, K1)
    R2 = xor_string(f1, L1)
    L2 = R1

    # Second round of Feistel
    f2 = xor_string(R2, K2)
    R3 = xor_string(f2, L2)
    L3 = R2

    return formatuuid(bin_to_hex(L3 + R3))


def decription(uuid, key):
    """
    black magic decription.
    """
    uuid = reverse_uuid(uuid)
    key = reverse_uuid(key)
    return encryption(uuid, key)
