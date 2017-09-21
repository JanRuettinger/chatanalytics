import pytest
import project.main.data_analytics as d_a
import json
import os

def test_androind_german(datadir):

  file = datadir.join('android_german.txt')
  android_german_data = file.read()

  android_german_exp_result = json.load(datadir.join('result_android_german.json'))

  df = d_a.preprocess_data(android_german_data)
  assert df.shape == (112,3)

  result_total_numbers = d_a.calculate_total_numbers(df)
  result_averages = d_a.calculate_averages(df)

  for key, value in result_total_numbers.items():
      assert round(value, 2) == round(android_german_exp_result[key], 2)

  for key, value in result_averages.items():
      assert round(value, 2) == round(android_german_exp_result[key], 2)

  d_a.make_plots(d_a.calculate_activity(df), str(datadir))
  assert os.path.isfile(datadir.strpath + '/plot1.png') == True
  assert os.path.isfile(datadir.strpath + '/plot2.png') == True
  assert os.path.isfile(datadir.strpath + '/plot3.png') == True
  assert os.path.isfile(datadir.strpath + '/plot4.png') == True
  assert os.path.isfile(datadir.strpath + '/plot5.png') == True


def test_ios_english(datadir):
  file = datadir.join('ios_english.txt')
  ios_english_data = file.read()

  ios_english_exp_result = json.load(datadir.join('result_ios_english.json'))

  df = d_a.preprocess_data(ios_english_data)
  assert df.shape == (3404, 3)

  result_total_numbers = d_a.calculate_total_numbers(df)
  result_averages = d_a.calculate_averages(df)

  for key, value in result_total_numbers.items():
      assert round(value, 2) == round(ios_english_exp_result[key], 2)

  for key, value in result_averages.items():
      assert round(value, 2) == round(ios_english_exp_result[key], 2)

  d_a.make_plots(d_a.calculate_activity(df), str(datadir))
  assert os.path.isfile(datadir.strpath + '/plot1.png') == True
  assert os.path.isfile(datadir.strpath + '/plot2.png') == True
  assert os.path.isfile(datadir.strpath + '/plot3.png') == True
  assert os.path.isfile(datadir.strpath + '/plot4.png') == True
  assert os.path.isfile(datadir.strpath + '/plot5.png') == True
