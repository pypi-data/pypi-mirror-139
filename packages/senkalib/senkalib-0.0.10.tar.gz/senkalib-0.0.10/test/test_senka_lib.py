import re
import unittest
from unittest.mock import *
from senkalib.chain.bsc.bsc_transaction_generator import BscTransactionGenerator
from senkalib.chain.osmosis.osmosis_transaction_generator import OsmosisTransactionGenerator
from senkalib.senka_lib import SenkaLib
import os

class TestSenkaLib(unittest.TestCase):
  def test_get_available_chain(self):
    with patch.object(os, 'listdir', new=TestSenkaLib.mock_listdir):
      chains = SenkaLib.get_available_chain()

      self.assertEqual(chains[0], BscTransactionGenerator)
      self.assertEqual(chains[1], OsmosisTransactionGenerator)

  def test_get_token_original_ids(self):
    token_original_ids_df = SenkaLib.get_token_original_ids()
    result = token_original_ids_df\
      .query('chain == "osmosis" and original_id == "ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2"')
    self.assertEqual(token_original_ids_df['uuid'][0], 'e7816a15-ce91-0aa8-0508-21d0d19f3aa8')

  @classmethod
  def mock_listdir(cls, transaction_hash):
    return ['osmosis', 'bsc']

if __name__ == '__main__':
  unittest.main()
