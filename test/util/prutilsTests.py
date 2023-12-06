#class DropNaTest(TestCase):
#
#    @staticmethod
#    def dropna_rows(df, *args):
#        return df[foldr(and_, args)]
#
#    def setUp(self):
#        df = pd.DataFrame({'Name': ['Alice', 'Bob', 'Charlie'],
#                           'Age': [25, nan, 30],
#                           'Salary': [50000, 60000, nan]
#                           })
#
#    def test(self, df):
#        """dropna_timeranges should be equivalent to dropping them using a for-loop."""
#        output = ''
#        for x in dropna_timeranges(df).iloc:
#            output += f"{x['desde']}, {x['hasta']}\n"
#
#        output2 = ''
#        for x in DropNaTest.dropna_rows(df, df['desde'].notna(), df['hasta'].notna()).iloc:
#            output2 += f"{x['desde']}, {x['hasta']}\n"
#
#        self.assertEquals(output2, output)
#