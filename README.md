# Weargaroo
Make your own solar -powered smart watch! Built with the [Seeeduino XIAO BLE Sense](https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html) microcontroller, this watch can be programmed in either Arduino or CircuitPython. For the purposes of this project we will be using CircuitPython.

# Features
 * **Color Screen** (240x240 RGB TFT via SPI)
 * **GPS** (receives lat, lng, alt, date, time, velocity, position of satellites, etc. via UART)
 * **Acceleromenter & Gyroscope** (for running cadence, step counting, fall detection, detecting motion/position etc. via I2C)
 * **Heart Rate Monitor** (receives raw analog data based on intensity of reflected light via AnalogIn)
 * **Microphone** (via PDM In)
 * **3 buttons** (via Digital Pins with internal pull-up)
 * **Vibrational Motor** (via AnalogOut/DigitalOut)
 * **120mAh LiPo Battery** (connected to builtin battery charging pins)
 * **Solar Panels** (wired in series and connected to boost converter to 5V in. not currently working)

# Software
  * [KICAD](https://www.kicad.org/) (free PCB Design Software)
  * [Fusion 360](https://www.autodesk.com/products/fusion-360/overview?term=1-YEAR&tab=subscription) (free CAD Software)
  * [Mu](https://codewith.mu/) (free CircuitPython IDE)
  * [PyCharm](https://www.jetbrains.com/pycharm/download) (free fully fledged Python IDE)
  * [Gimp](https://www.gimp.org/) (free Image Editor)
  * [Ultimaker Cura](https://ultimaker.com/software/ultimaker-cura) (free gcode 3D print setup software)
  * [git](https://git-scm.com/downloads) (free version control software)

# Resources
  * [Seeed Studio Official Documentation](https://wiki.seeedstudio.com/XIAO_BLE/)
  * [CircuitPython Official Documentation](https://docs.circuitpython.org/en/latest/README.html)
  * [Interpreting NMEA Sentences (for GPS)](http://aprs.gids.nl/nmea/#allgp)
  * [Making Bitmaps](https://learn.adafruit.com/creating-your-first-tilemap-game-with-circuitpython/indexed-bmp-graphics)

# Components
|  Item                       |  Reference |  Quantity  | Price | Shipping | Features  | Price at Scale |                                                              
|:----------------------------|:------| :------------|:---------------|:---------|:-------------------------------------------------------------------------|:----|
| *[Seeed XIAO BLE nRF52840 Sense](https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html)| [nRF2580](https://www.nordicsemi.com/products/nrf52840#:~:text=The%20nRF52840%20is%20fully%20multiprotocol,unit%20running%20at%2064%20MHz.) | 1           | $15.99         | $8.99    | BLE, MicroPython, 6-axis IMU, Microphone, Battery Charger, 5uA sleep mode| [$13.90](https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html) |
| [MakerFocus 1.3", 240 x 240 Color TFT](https://www.amazon.com/dp/B07P9X3L7M?ref_=cm_sw_r_cp_ud_dp_WN15FXJF4QTTX7NJ339R)| ST7789 | 1 | $12.99 | $0 (w/ Prime) | square, color, backlight, easy to use | [$3.78](https://www.aliexpress.com/item/2255800357390105.html?spm=a2g0o.productlist.0.0.171d6d91xjum1Q&algo_pvid=f7e25705-3e88-4500-96e8-95d158f577bb&algo_exp_id=f7e25705-3e88-4500-96e8-95d158f577bb-2&pdp_ext_f=%7B%22sku_id%22%3A%2212000020110706989%22%7D&pdp_npi=2%40dis%21USD%21%213.2%21%21%21%21%21%402101e9d416568093275105725eb1c7%2112000020110706989%21sea) |
| [Gooouuuunu Tech GPS module](https://www.amazon.com/dp/B084MK8BS2?ref_=cm_sw_r_cp_ud_dp_SF6SBXN5FPV1GJ83TW89) | [GT-U7](https://manuals.plus/goouuu/goouuu-tech-gt-u7-gps-modules#axzz7Xvpu67Gv) | 1 | $11.59 | $0 (w/ Prime) | GPS with antenna, 2.5m accuracy | [$5.49](https://www.aliexpress.com/item/3256802640836752.html?spm=a2g0o.productlist.0.0.2644396buUZ6GM&algo_pvid=fd4ad6fe-175c-4408-8699-b3b894e73c04&algo_exp_id=fd4ad6fe-175c-4408-8699-b3b894e73c04-0&pdp_ext_f=%7B%22sku_id%22%3A%2212000022363403421%22%7D&pdp_npi=2%40dis%21USD%21%215.49%21%21%21%21%21%4021031a5516568094154314210e8e5b%2112000022363403421%21sea) |
| [Pulse Sensor Arduino Heart Rate Sensor](https://www.amazon.com/Sensor-Arduino-Photoelectric-Reflective-Mega2560/dp/B09NQ9WGCY/ref=sr_1_12?crid=3F5ZNSU4TX29R&keywords=pulse+sensor&qid=1653876417&s=industrial&sprefix=pulse+sensor%2Cindustrial%2C123&sr=1-12) | N/A | 1 | $8.99 | $0 (w/ Prime) | small analog pulse sensor | [$1.38](https://www.aliexpress.com/item/3256801714815056.html?spm=a2g0o.productlist.0.0.6fc416e73ysCID&algo_pvid=8e2a94e9-1683-4e7f-9d0d-58e9d17f59df&aem_p4p_detail=202207021751463864511755417600038484100&algo_exp_id=8e2a94e9-1683-4e7f-9d0d-58e9d17f59df-7&pdp_ext_f=%7B%22sku_id%22%3A%2212000018063116288%22%7D&pdp_npi=2%40dis%21USD%21%211.35%21%21%21%21%21%402101e9cf16568095067077061e0813%2112000018063116288%21sea) |
| [120 mAh LiPo Battery](https://www.amazon.com/dp/B07TXHM388?ref_=cm_sw_r_cp_ud_dp_SR0F0YEB0Q4N4QTFMQW3) | [PL521521](https://www.ctechigroup.com/brand-lithium-ion-polymer-battery-pl521521-3-7v-2) | 1 | $8.39 | $0 (w/ Prime) | 3.7V, 120mAh | [$4.14](https://www.aliexpress.com/item/2251832628155410.html?spm=a2g0o.productlist.0.0.5f83353dO3ziJI&algo_pvid=2d86ddfb-45da-47a7-8492-946ff3bcb2fd&algo_exp_id=2d86ddfb-45da-47a7-8492-946ff3bcb2fd-0&pdp_ext_f=%7B%22sku_id%22%3A%2264650542491%22%7D&pdp_npi=2%40dis%21USD%21%214.24%21%21%21%21%21%402101e9d216568095962576570ec69e%2164650542491%21sea) | 
| [Vibrational Motor](https://www.amazon.com/dp/B07Q1ZV4MJ?ref_=cm_sw_r_cp_ud_dp_SFZ0MC2BX6PRQMFXA749) | N/A | 1 | $7 | $0 (w/Prime) | works on analog or digital output pins | [$0.20](https://www.aliexpress.com/item/3256803067070784.html?spm=a2g0o.productlist.0.0.21e35ea8hr526m&algo_pvid=0459b573-d698-42f1-a481-4e5f5d482edb&aem_p4p_detail=2022070218025517437213330786600008351212&algo_exp_id=0459b573-d698-42f1-a481-4e5f5d482edb-3&pdp_ext_f=%7B%22sku_id%22%3A%2212000024870520552%22%7D&pdp_npi=2%40dis%21USD%21%212.15%21%21%21%21%21%402101d8f416568101758498616e040c%2112000024870520552%21sea) |
| [Momentary Buttons](https://a.co/d/0rG6baG) | N/A | 3 | $7 | $0 (w/Prime) | Momentary Buttons | [$0.15](https://www.aliexpress.com/item/2251832628155410.html?spm=a2g0o.productlist.0.0.5f83353dO3ziJI&algo_pvid=2d86ddfb-45da-47a7-8492-946ff3bcb2fd&algo_exp_id=2d86ddfb-45da-47a7-8492-946ff3bcb2fd-0&pdp_ext_f=%7B%22sku_id%22%3A%2264650542491%22%7D&pdp_npi=2%40dis%21USD%21%214.24%21%21%21%21%21%402101e9d216568095962576570ec69e%2164650542491%21sea) |
| [Flexible PLA](https://a.co/d/bo6UFFs) | FPLA | 1 | $33 | $0 (w/ Prime) | flexible brown PLA | ~$2 |
| [Custom PCB](https://oshpark.com/home) | N/A | 3 | $15.70 | $5 | 0.8mm | ~3 |
| **[Solar Cells](https://www.digikey.com/short/2nrbbhjb) | [IXOLARTM SolarBITs](https://waf-e.dubudisk.com/anysolar.dubuplus.com/techsupport@anysolar.biz/O18Adzn/DubuDisk/www/Gen2/KXOB25-12X1F%20DATA%20SHEET%20202007.pdf) |  10 | $29.4 | $4.99 | 0.56V, 24.5mW | [$18.7](https://www.digikey.com/short/2nrbbhjb) |
| **[Boost Converter](https://a.co/d/iBbj18a) | N/A | 5 | $7.99 | $0 (w/ Prime) | 0.9-5V to 5V | [$0.5](https://www.aliexpress.com/item/3256803249225601.html?spm=a2g0o.productlist.0.0.41f51f92PbqCNL&algo_pvid=4f9b0908-b571-4540-ab84-a6b63eb70cf9&aem_p4p_detail=202207021759442215847245405600041852125&algo_exp_id=4f9b0908-b571-4540-ab84-a6b63eb70cf9-8&pdp_ext_f=%7B%22sku_id%22%3A%2212000025776960394%22%7D&pdp_npi=2%40dis%21USD%21%210.5%21%21%21%21%21%40210318b816568099840427637e8f1b%2112000025776960394%21sea) |


*$16 Seeed BLE can be replaced by $6 Seeed if bluetooth, accelerometer, and gyroscope are not desired<br>
** Adding solar panels costs ~$40 and has so far not been effective


# Supplies
<hr>

| Item | Price |
|:-----|:------|
| [Soldering Iron](https://www.amazon.com/dp/B07S61WT16?ref_=cm_sw_r_cp_ud_dp_9QCDJ8K50YN0SA9NXVT3) | $21 |
| [Wire Strippers](https://www.amazon.com/dp/B07D25N45F?ref_=cm_sw_r_cp_ud_dp_9H7ZDP3K031YC7EBBG75) | $7 |
| [Solder](https://www.amazon.com/dp/B09KM2LW4G?ref_=cm_sw_r_cp_ud_dp_CRJENFVCX6DY4KYW6DFN) | $7 |
| [Small Gauge Wire (30)](https://www.amazon.com/dp/B01KQ2JNLI?ref_=cm_sw_r_cp_ud_dp_46RT5XTP5HQKB0TX04W2) | $13 |
| [Ender 3 Pro 3D Printer](https://a.co/d/czNa5k4) | $236 |
| [Gorilla Glue Gel](https://a.co/d/igLpw8D) | $8 |

# Price
* Without solar panels the components in the watch cost ~$70 or ~$40 if produced at scale.
* When building just one there will be some waste (e.g. you have to buy PCBs in batches of 3)
* Without solar panels, accelerometer, gyro, ble, or heart rate a gps watch could be made for ~$55, or ~$30 at scale.
* The simplest smart watch requires only a $6 Seeed, a $13 screen ($4 at scale), and a 3D printed band and could be produced for ~$20 or ~$10 at scale.
* Solar panels add ~$40 to the price and so far have not been effective (but I'm holding out hope).

# Pinout
| Component | Part Pin | Board Pin |
| :---------|:---------|:----------|
| Screen    | SCL      | SCK       |
| Screen    | SDA      | MOSI      |
| Screen    | Res      | D4        |
| Screen    | DC       | D5        |
| GT-U7     | TXD      | RX        |
| Bottom Button | +    | *A0        |
| Middle Button | +    | A1        |
| Top Button | +    | A2        |
| Vibrational Motor | + | *A0 |
| Pulse | Signal | A3|

# Notes

### Screen
* the silkscreen on the PCB says SCL and SDA implying the screen uses I2C, but these pins actually get connected to SCK and MOSI and the screen uses SPI
* screen SPI needs `polarity=1`, `phase=1`. In Arduino, this is `SPI_MODE3`
* To display images, use GIMP to convert the image to an indexed bitmap, the fewer the colors used the better (recommended <10 colors) (see https://learn.adafruit.com/creating-your-first-tilemap-game-with-circuitpython/indexed-bmp-graphics)

### IMU
 * The internal IMU works using I2C. Before reading data, power the IMU and allow time to sleep before initializing (see `accel.py`)

### GPS
 * Make sure `TX` on the GPS is wired to `RX` on the Seeed

### Vibrational Motor / Bottom Button
 * The vibrational motor and the bottom button use the same pin `A0`, so only one can be used at onse.



# Getting Started

### Building Hardware
Unfortunately the pads on the custom PCB do not fit the Seeed quite right so soldering will be tough but possible.
The next revision of the board should improve this.

### Booting
To boot the Seeed:
 * double click the boot button (located on right side of USB-C port).
 * a File Explorer window should pop up on your computer with a CircuitPython D: drive
 * drag and drop `boot/adafruit-circuitpython-Seeed_XIAO_nRF52840_Sense-en_US-20220607-ee3ccbc.uf2` into the CircuitPython folder
 * once the `.uf2` file gets loaded, the device will boot up and a new File Explorer window should pop up, now showing a folder containing code.py and a `lib` folder
 * copy and paste the contents of `src` into the CircuitPython device folder

### Running Code
When the Seeed is turned on or rebooted, either `code.py` or `main.py` will be run. 
The easiest way to test code is to use the Mu Editor in RP2040 Mode.
You can run files individually with the Run button, or use the REPL to test stuff.


### Interested in a Doing It Yourself?
If you are interested in this idea and want to do some or all of this project on your own, I'd love to hear about it.
I am toying with the idea of selling kits of materials as well, so let me know if you are interested!
<a href="mailto:modularizer@gmail.com">modularizer@gmail.com</a>