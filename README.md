# USB Protect for HamoniKR Linux

* 시스템에 부착된 여러가지 장치의 차단을 설정하는 프로그램입니다.
* 장치의 종류로 차단하는 방법은 `프로그램>장치 차단 설정`을 실행하면 다음과 같은 화면이 나오고 체크한 후 확인 버튼을 누르면 적용됩니다.
* 만약 특정 제품만 차단하고 싶은 경우에는 직접 설정파일을 수정해서 적용할 수 있습니다. (`20-allow-idVendor.rules` 파일과 `30-usb-lockdown.rules` 파일을 자신의 상황에 맞게 수정)


![app](./img/app.png)

# Developer

HamoniKR Team <pkg@hamonikr.org>

# 라이선스

GPL-2.0

# 설치

```
sudo apt install hamonikr-lockdown
```

# 사용법

아래 두 파일에 장치 제어 설정이 있습니다.
* 20-allow-idVendor.rules.EXAMPLE
* 30-usb-lockdown.rules.EXAMPLE

다음과 같이 복사한 후 `20-allow-idVendor.rules` 파일과 `30-usb-lockdown.rules` 파일을 자신의 상황에 맞게 수정 후 사용하면 됩니다.

```
sudo cp /etc/udev/rules.d/20-allow-idVendor.rules.EXAMPLE /etc/udev/rules.d/20-allow-idVendor.rules
sudo cp /etc/udev/rules.d/30-usb-lockdown.rules.EXAMPLE /etc/udev/rules.d/30-usb-lockdown.rules

```

자신의 usb의 정보를 알기 위해서는 해당 장치를 컴퓨터에 삽입한 후 lsusb 명령을 이용하세요.

# Debug

```tail -f /tmp/usb-lockdown.log```

## lockdown 
장치를 사용할 수 없도록 하기 위해서는 /sys$devpath/authorized 값을 0으로 변경
$devpath : 현재 검색된 장치의 경로

차단 메시지를 보이고 싶은 경우에는 아래 내용을 추가
ENV{DISPLAY}=":0.0", RUN+="/usr/local/bin/usb-unauthorized"

## Refrences
* https://usb.org/defined-class-codes
* https://www.beyondlogic.org/usbnutshell/usb5.shtml
 
* Authorizing (or not) your USB devices to connect to the system
* https://www.kernel.org/doc/Documentation/usb/authorization.txt
 
## USB 장치의 유형으로 제어를 하는 경우

* Ref : https://usb.org/defined-class-codes
* Ref : https://www.beyondlogic.org/usbnutshell/usb5.shtml

ALLOW all hid(keyboard, mouse) - bInterfaceClass : 03
ALLOW all printer - bInterfaceClass : 07
ALLOW all usb hub - bInterfaceClass : 09
ALLOW all Video device - bInterfaceClass : 0E

# 주의
장치의 종류로 차단하거나 장치의 제품명으로 차단하는 기능을 
각각 사용할 수 있지만 두가지를 결합해서는 사용할 수 없음.

장치의 유형으로 제어한 부분이 가장 마지막에 실행되기 때문에
제품명으로 차단하고 싶은 경우에는 키보드, 마우들 모든 필요한 장치의 제품명을 등록해서 허용해야 함.

## 모든 장치 허용 시
```
find /sys -name "authorized*" | while read i; do echo 1 | sudo tee $i; done
```

## 모든 장치의 차단값 보기
```
find /sys -name "authorized*" | while read i; do echo "$i $(cat $i)"; done
```
