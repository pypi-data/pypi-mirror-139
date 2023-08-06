# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google_trans_new_that_works']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'urllib3>=1.26.8,<2.0.0']

setup_kwargs = {
    'name': 'google-trans-new-that-works',
    'version': '0.1.1',
    'description': 'Google translate that works ( i think )',
    'long_description': '# google_trans_new\n### Version 1.1.9\n\nA free and unlimited python API for google translate.  \nIt\'s very easy to use and solve the problem that the old api which use tk value cannot be used.  \nThis interface is for academic use only, please do not use it for commercial use.  \n  \nVersion 1.1.9 have fixed url translate.\nPs:\nIf your get translations for different genders, it will return a list.\nhttps://support.google.com/translate/answer/9179237?p=gendered_translations&hl=zh-Hans&visit_id=637425624803913067-1347870216&rd=1\n***\n  \n  \nInstallation\n====\n```\npip install google_trans_new\n```\n***\n  \n  \nBasic Usage\n=====\n### Translate\n```python\nfrom google_trans_new import google_translator  \n  \ntranslator = google_translator()  \ntranslate_text = translator.translate(\'สวัสดีจีน\',lang_tgt=\'en\')  \nprint(translate_text)\n-> Hello china\n```\n***\n\nAdvanced Usage\n=====\n### Translate \n```python  \nfrom google_trans_new import google_translator  \n\n# You can set the url_suffix according to your country. You can set url_suffix="hk" if you are in hong kong,url_suffix use in https://translate.google.{url_suffix}/ \n# If you want use proxy, you can set proxies like proxies={\'http\':\'xxx.xxx.xxx.xxx:xxxx\',\'https\':\'xxx.xxx.xxx.xxx:xxxx\'}\ntranslator = google_translator(url_suffix="hk",timeout=5,proxies={\'http\':\'xxx.xxx.xxx.xxx:xxxx\',\'https\':\'xxx.xxx.xxx.xxx:xxxx\'})  \n# <Translator url_suffix=cn timeout=5 proxies={\'http\':\'xxx.xxx.xxx.xxx:xxxx\',\'https\':\'xxx.xxx.xxx.xxx:xxxx\'}>  \n#  default parameter : url_suffix="cn" timeout=5 proxies={}\ntranslate_text = translator.translate(\'สวัสดีจีน\',lang_tgt=\'zh\')  \n# <Translate text=สวัสดีจีน lang_tgt=th lang_src=zh>  \n#  default parameter : lang_src=auto lang_tgt=auto \n#  API can automatically identify the src translation language, so you don’t need to set lang_src\nprint(translate_text)\n-> 你好中国\n```\n### Multithreading Translate\n\n```python\nfrom google_trans_new import google_translator\nfrom multiprocessing.dummy import Pool as ThreadPool\nimport time\n\npool = ThreadPool(8)  # Threads\n\n\ndef request(text):\n    lang = "zh"\n    t = google_translator(timeout=5)\n    translate_text = t.translate(text.strip(), lang)\n    return translate_text\n\n\nif __name__ == "__main__":\n    time1 = time.time()\n    with open("tests/test.txt", \'r\') as f_p:\n        texts = f_p.readlines()\n        try:\n            results = pool.map(request, texts)\n        except Exception as e:\n            raise e\n        pool.close()\n        pool.join()\n\n        time2 = time.time()\n        print("Translating %s sentences, a total of %s s" % (len(texts), time2 - time1))\n-> Translating\n720\nsentences, a\ntotal\nof\n25.89591908454895\ns \n```\n### Detect\n```python\nfrom google_trans_new import google_translator  \n  \ndetector = google_translator()  \ndetect_result = detector.detect(\'สวัสดีจีน\')\n# <Detect text=สวัสดีจีน >  \nprint(detect_result)\n-> [\'th\', \'thai\']\n```\n### Pronounce\n```python\nfrom google_trans_new import google_translator  \n  \ntranslator  = google_translator()  \nPronounce = translator.translate(\'สวัสดีจีน\',lang_src=\'th\',lang_tgt=\'zh\',pronounce=True)  \nprint(Pronounce)\n-> [\'你好中国 \', \'S̄wạs̄dī cīn\', \'Nǐ hǎo zhōngguó\']\n```\n***\n\nPrerequisites\n====\n* **Python >=3.6**  \n* **requests**  \n* **six**  \n***\n  \n  \nLicense\n====\ngoogle_trans_new is licensed under the MIT License. The terms are as follows:  \n\n```\nMIT License  \n\nCopyright (c) 2020 lushan88a  \n\nPermission is hereby granted, free of charge, to any person obtaining a copy  \nof this software and associated documentation files (the "Software"), to deal  \nin the Software without restriction, including without limitation the rights  \nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell  \ncopies of the Software, and to permit persons to whom the Software is  \nfurnished to do so, subject to the following conditions:  \n\nThe above copyright notice and this permission notice shall be included in all  \ncopies or substantial portions of the Software.  \n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  \nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  \nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  \nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  \nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  \nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  \nSOFTWARE.  \n```\n',
    'author': 'Sayan Biswas',
    'author_email': 'sayan@intellivoid.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AnimeKaizoku/google_trans_new',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
