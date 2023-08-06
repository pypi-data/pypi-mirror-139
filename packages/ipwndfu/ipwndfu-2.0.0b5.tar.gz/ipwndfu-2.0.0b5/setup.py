# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ipwndfu', 'libusbfinder']

package_data = \
{'': ['*'], 'ipwndfu': ['bin/*'], 'libusbfinder': ['bottles/*']}

install_requires = \
['cryptography>=36.0.1,<37.0.0', 'pyusb>=1.2.1,<2.0.0']

entry_points = \
{'console_scripts': ['ipwndfu = ipwndfu.main:main']}

setup_kwargs = {
    'name': 'ipwndfu',
    'version': '2.0.0b5',
    'description': 'The DFU exploitation toolkit for Apple devices',
    'long_description': "![](.github/ipwndfu.png)\n\n# Open-source jailbreaking tool for many iOS devices\n\n# Cause there's no such thing as Good Silicon. Only Bad tests.\n\n**Read [disclaimer](#disclaimer) before using this software.*\n\n## About this fork\n\nThis fork is maintained by the hack-different team and is gladly accepting PRs from the wider community. All of the\noriginal credit go to axi0mx et al.\n\n## checkm8\n\n* permanent unpatchable bootrom exploit for hundreds of millions of iOS devices\n\n* meant for researchers, this is not a jailbreak with Cydia yet\n\n* allows dumping SecureROM, decrypting keybags for iOS firmware, and demoting device for JTAG\n\n* current SoC support: s5l8947x, s5l8950x, s5l8955x, s5l8960x, t7000, s8000, t8002, s8003, t8004, t8010, t8011, t8012,\n  t8015\n\n* future SoC support: s5l8940x, s5l8942x, s5l8945x, s5l8747x, t7001, s7002, s8001\n\n* full jailbreak with Cydia on latest iOS version is possible, but requires additional work\n\n## Quick start guide for checkm8\n\n1. Use a cable to connect device to your Mac. Hold buttons as needed to enter DFU Mode.\n\n2. First run ```./ipwndfu -p``` to exploit the device. Repeat the process if it fails, it is not reliable.\n\n3. Run ```./ipwndfu --dump-rom``` to get a dump of SecureROM.\n\n4. Run ```./ipwndfu --decrypt-gid KEYBAG``` to decrypt a keybag.\n\n5. Run ```./ipwndfu --demote``` to demote device and enable JTAG.\n\n## About this fork (addendum)\n\nThis fork supports the t8012 chip. It is based on\n[LinusHenze's ipwndfu patches](https://github.com/LinusHenze/ipwndfu_public), which allow it to boot iBoot without\ndestroying the heap. A simple patch that allows you to boot any extracted iBoot image (without the img4 wrapper) is\nprovided in `nop_image4.py`, which was based on LinusHenze's `rmsigchks.py`.\n\n## Features\n\n* Jailbreak and downgrade iPhone 3GS (new bootrom) with alloc8 untethered bootrom exploit. :-)\n\n* Pwned DFU Mode with steaks4uce exploit for S5L8720 devices.\n\n* Pwned DFU Mode with limera1n exploit for S5L8920/S5L8922 devices.\n\n* Pwned DFU Mode with SHAtter exploit for S5L8930 devices.\n\n* Dump SecureROM on S5L8920/S5L8922/S5L8930 devices.\n\n* Dump NOR on S5L8920 devices.\n\n* Flash NOR on S5L8920 devices.\n\n* Encrypt or decrypt hex data on a connected device in pwned DFU Mode using its GID or UID key.\n\n## Dependencies\n\nThis tool should be compatible with Mac and Linux. It won't work in a virtual machine.\n\n* libusb, `If you are using Linux: install libusb using your package manager.`\n* [iPhone 3GS iOS 4.3.5 iBSS](#ibss)\n\n## Tutorial\n\nThis tool can be used to downgrade or jailbreak iPhone 3GS (new bootrom) without SHSH blobs, as documented\nin [JAILBREAK-GUIDE](https://github.com/axi0mX/ipwndfu/blob/master/JAILBREAK-GUIDE.md).\n\n## Exploit write-up\n\nWrite-up for alloc8 exploit can be found here:\n\nhttps://github.com/axi0mX/alloc8\n\n## iBSS\n\nDownload iPhone 3GS iOS 4.3.5 IPSW from Apple:\n\nhttp://appldnld.apple.com/iPhone4/041-1965.20110721.gxUB5/iPhone2,1_4.3.5_8L1_Restore.ipsw\n\nIn Terminal, extract iBSS using the following command, then move the file to ipwndfu folder:\n\n```\nunzip -p iPhone2,1_4.3.5_8L1_Restore.ipsw Firmware/dfu/iBSS.n88ap.RELEASE.dfu > n88ap-iBSS-4.3.5.img3\n```\n\n## Coming soon!\n\n* Reorganize and refactor code.\n\n* Easier setup: download iBSS automatically using partial zip.\n\n* Dump SecureROM on S5L8720 devices.\n\n* Install custom boot logos on devices jailbroken with 24Kpwn and alloc8.\n\n* Enable verbose boot on devices jailbroken with 24Kpwn and alloc8.\n\n## Disclaimer\n\n**This is BETA software.**\n\nBackup your data.\n\nThis tool is currently in beta and could potentially brick your device. It will attempt to save a copy of data in NOR to\nnor-backups folder before flashing new data to NOR, and it will attempt to not overwrite critical data in NOR which your\ndevice requires to function. If something goes wrong, hopefully you will be able to restore to latest IPSW in iTunes and\nbring your device back to life, or use nor-backups to restore NOR to the original state, but I cannot provide any\nguarantees.\n\n**There is NO warranty provided.**\n\nTHERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW. THE ENTIRE RISK AS TO THE QUALITY AND\nPERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY\nSERVICING, REPAIR OR CORRECTION.\n\n## Toolchain\n\nYou will not need to use `make` or compile anything to use ipwndfu. However, if you wish to make changes to assembly\ncode in `src/*`, you will need to use an ARM toolchain and assemble the source files by running `make`.\n\nIf you are using macOS with Homebrew, you can use binutils and gcc-arm-embedded. You can install them with these\ncommands:\n\n```\nbrew install binutils\nbrew cask install https://raw.githubusercontent.com/Homebrew/homebrew-cask/b88346667547cc85f8f2cacb3dfe7b754c8afc8a/Casks/gcc-arm-embedded.rb\n```\n\n## Credit\n\ngeohot for limera1n exploit\n\nposixninja and pod2g for SHAtter exploit\n\nchronic, CPICH, ius, MuscleNerd, Planetbeing, pod2g, posixninja, et al. for 24Kpwn exploit\n\npod2g for steaks4uce exploit\n\nwalac for pyusb\n\ncheckra1n team, littlelailo for the idea of just removing the call to image4_load\n",
    'author': 'axi0mX',
    'author_email': 'axi0mXor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
