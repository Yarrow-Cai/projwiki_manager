#!/usr/bin/env python3
"""
更新AI任务文件中的路径映射
"""

import json
import sys
from pathlib import Path

# 路径映射表
PATH_MAPPING = {
    # Application层
    ".zed\\.projwiki\\modules\\main.md": ".zed\\.projwiki\\modules\\application\\main.md",
    ".zed\\.projwiki\\modules\\global.md": ".zed\\.projwiki\\modules\\application\\global.md",
    ".zed\\.projwiki\\modules\\systick.md": ".zed\\.projwiki\\modules\\application\\systick.md",
    ".zed\\.projwiki\\modules\\gd32h75e_it.md": ".zed\\.projwiki\\modules\\application\\gd32h75e_it.md",
    # Middleware - EtherCAT
    ".zed\\.projwiki\\modules\\ecatappl.md": ".zed\\.projwiki\\modules\\middleware\\ethercat\\ecatappl.md",
    ".zed\\.projwiki\\modules\\ecatslv.md": ".zed\\.projwiki\\modules\\middleware\\ethercat\\ecatslv.md",
    ".zed\\.projwiki\\modules\\ecatcoe.md": ".zed\\.projwiki\\modules\\middleware\\ethercat\\ecatcoe.md",
    ".zed\\.projwiki\\modules\\coeappl.md": ".zed\\.projwiki\\modules\\middleware\\ethercat\\coeappl.md",
    ".zed\\.projwiki\\modules\\cia402appl.md": ".zed\\.projwiki\\modules\\middleware\\ethercat\\cia402appl.md",
    ".zed\\.projwiki\\modules\\mailbox.md": ".zed\\.projwiki\\modules\\middleware\\ethercat\\mailbox.md",
    ".zed\\.projwiki\\modules\\sdoserv.md": ".zed\\.projwiki\\modules\\middleware\\ethercat\\sdoserv.md",
    ".zed\\.projwiki\\modules\\objdef.md": ".zed\\.projwiki\\modules\\middleware\\ethercat\\objdef.md",
    ".zed\\.projwiki\\modules\\gdesc.md": ".zed\\.projwiki\\modules\\middleware\\ethercat\\gdesc.md",
    ".zed\\.projwiki\\modules\\esc_exti.md": ".zed\\.projwiki\\modules\\middleware\\ethercat\\esc_exti.md",
    ".zed\\.projwiki\\modules\\esc_timer.md": ".zed\\.projwiki\\modules\\middleware\\ethercat\\esc_timer.md",
    # Middleware - USB Device Core
    ".zed\\.projwiki\\modules\\usbd_core.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\core\\usbd_core.md",
    ".zed\\.projwiki\\modules\\usbd_enum.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\core\\usbd_enum.md",
    ".zed\\.projwiki\\modules\\usbd_transc.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\core\\usbd_transc.md",
    # Middleware - USB Device Driver
    ".zed\\.projwiki\\modules\\drv_usbd_int.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\driver\\drv_usbd_int.md",
    ".zed\\.projwiki\\modules\\drv_usb_core.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\driver\\drv_usb_core.md",
    ".zed\\.projwiki\\modules\\drv_usb_dev.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\driver\\drv_usb_dev.md",
    # Middleware - USB Device Class
    ".zed\\.projwiki\\modules\\audio_core.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\class\\audio_core.md",
    ".zed\\.projwiki\\modules\\audio_out_itf.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\class\\audio_out_itf.md",
    ".zed\\.projwiki\\modules\\cdc_acm_core.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\class\\cdc_acm_core.md",
    ".zed\\.projwiki\\modules\\custom_hid_core.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\class\\custom_hid_core.md",
    ".zed\\.projwiki\\modules\\standard_hid_core.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\class\\standard_hid_core.md",
    ".zed\\.projwiki\\modules\\dfu_core.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\class\\dfu_core.md",
    ".zed\\.projwiki\\modules\\dfu_mem.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\class\\dfu_mem.md",
    ".zed\\.projwiki\\modules\\usbd_msc_core.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\class\\usbd_msc_core.md",
    ".zed\\.projwiki\\modules\\usbd_msc_bbb.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\class\\usbd_msc_bbb.md",
    ".zed\\.projwiki\\modules\\usbd_msc_scsi.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\class\\usbd_msc_scsi.md",
    ".zed\\.projwiki\\modules\\usb_iap_core.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\class\\usb_iap_core.md",
    ".zed\\.projwiki\\modules\\printer_core.md": ".zed\\.projwiki\\modules\\middleware\\usb\\device\\class\\printer_core.md",
    # Middleware - USB Host Core
    ".zed\\.projwiki\\modules\\usbh_core.md": ".zed\\.projwiki\\modules\\middleware\\usb\\host\\core\\usbh_core.md",
    ".zed\\.projwiki\\modules\\usbh_enum.md": ".zed\\.projwiki\\modules\\middleware\\usb\\host\\core\\usbh_enum.md",
    ".zed\\.projwiki\\modules\\usbh_pipe.md": ".zed\\.projwiki\\modules\\middleware\\usb\\host\\core\\usbh_pipe.md",
    ".zed\\.projwiki\\modules\\usbh_transc.md": ".zed\\.projwiki\\modules\\middleware\\usb\\host\\core\\usbh_transc.md",
    # Middleware - USB Host Driver
    ".zed\\.projwiki\\modules\\drv_usbh_int.md": ".zed\\.projwiki\\modules\\middleware\\usb\\host\\driver\\drv_usbh_int.md",
    ".zed\\.projwiki\\modules\\drv_usb_host.md": ".zed\\.projwiki\\modules\\middleware\\usb\\host\\driver\\drv_usb_host.md",
    # Middleware - USB Host Class
    ".zed\\.projwiki\\modules\\usbh_cdc_core.md": ".zed\\.projwiki\\modules\\middleware\\usb\\host\\class\\usbh_cdc_core.md",
    ".zed\\.projwiki\\modules\\usbh_hid_core.md": ".zed\\.projwiki\\modules\\middleware\\usb\\host\\class\\usbh_hid_core.md",
    ".zed\\.projwiki\\modules\\usbh_standard_hid.md": ".zed\\.projwiki\\modules\\middleware\\usb\\host\\class\\usbh_standard_hid.md",
    ".zed\\.projwiki\\modules\\usbh_msc_core.md": ".zed\\.projwiki\\modules\\middleware\\usb\\host\\class\\usbh_msc_core.md",
    ".zed\\.projwiki\\modules\\usbh_msc_bbb.md": ".zed\\.projwiki\\modules\\middleware\\usb\\host\\class\\usbh_msc_bbb.md",
    ".zed\\.projwiki\\modules\\usbh_msc_scsi.md": ".zed\\.projwiki\\modules\\middleware\\usb\\host\\class\\usbh_msc_scsi.md",
    ".zed\\.projwiki\\modules\\usbh_msc_fatfs.md": ".zed\\.projwiki\\modules\\middleware\\usb\\host\\class\\usbh_msc_fatfs.md",
    # Calculation层
    ".zed\\.projwiki\\modules\\foc.md": ".zed\\.projwiki\\modules\\calculation\\foc.md",
    ".zed\\.projwiki\\modules\\pid.md": ".zed\\.projwiki\\modules\\calculation\\pid.md",
    ".zed\\.projwiki\\modules\\fast_math.md": ".zed\\.projwiki\\modules\\calculation\\fast_math.md",
    ".zed\\.projwiki\\modules\\encoder.md": ".zed\\.projwiki\\modules\\calculation\\encoder.md",
    ".zed\\.projwiki\\modules\\motor_control.md": ".zed\\.projwiki\\modules\\calculation\\motor_control.md",
    ".zed\\.projwiki\\modules\\hard_ware.md": ".zed\\.projwiki\\modules\\calculation\\hard_ware.md",
    ".zed\\.projwiki\\modules\\inverter_hal.md": ".zed\\.projwiki\\modules\\calculation\\inverter_hal.md",
    # BSP - System
    ".zed\\.projwiki\\modules\\system_gd32h75e.md": ".zed\\.projwiki\\modules\\bsp\\system\\system_gd32h75e.md",
    ".zed\\.projwiki\\modules\\gd32h75e_err_report.md": ".zed\\.projwiki\\modules\\bsp\\system\\gd32h75e_err_report.md",
    ".zed\\.projwiki\\modules\\RTE_Components.md": ".zed\\.projwiki\\modules\\bsp\\system\\RTE_Components.md",
    # BSP - ESC Library
    ".zed\\.projwiki\\modules\\gd32h75e_esc_intc.md": ".zed\\.projwiki\\modules\\bsp\\esc_library\\gd32h75e_esc_intc.md",
    ".zed\\.projwiki\\modules\\gd32h75e_esc_ospi.md": ".zed\\.projwiki\\modules\\bsp\\esc_library\\gd32h75e_esc_ospi.md",
    ".zed\\.projwiki\\modules\\gd32h75e_esc_phy.md": ".zed\\.projwiki\\modules\\bsp\\esc_library\\gd32h75e_esc_phy.md",
    ".zed\\.projwiki\\modules\\gd32h75e_esc_pmu.md": ".zed\\.projwiki\\modules\\bsp\\esc_library\\gd32h75e_esc_pmu.md",
    ".zed\\.projwiki\\modules\\gd32h75e_esc_syscfg.md": ".zed\\.projwiki\\modules\\bsp\\esc_library\\gd32h75e_esc_syscfg.md",
    ".zed\\.projwiki\\modules\\gd32h75e_esc_timer.md": ".zed\\.projwiki\\modules\\bsp\\esc_library\\gd32h75e_esc_timer.md",
    # BSP - Standard Peripheral
    ".zed\\.projwiki\\modules\\gd32h75e_adc.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_adc.md",
    ".zed\\.projwiki\\modules\\gd32h75e_can.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_can.md",
    ".zed\\.projwiki\\modules\\gd32h75e_cmp.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_cmp.md",
    ".zed\\.projwiki\\modules\\gd32h75e_crc.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_crc.md",
    ".zed\\.projwiki\\modules\\gd32h75e_ctc.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_ctc.md",
    ".zed\\.projwiki\\modules\\gd32h75e_dac.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_dac.md",
    ".zed\\.projwiki\\modules\\gd32h75e_dbg.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_dbg.md",
    ".zed\\.projwiki\\modules\\gd32h75e_dma.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_dma.md",
    ".zed\\.projwiki\\modules\\gd32h75e_edout.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_edout.md",
    ".zed\\.projwiki\\modules\\gd32h75e_efuse.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_efuse.md",
    ".zed\\.projwiki\\modules\\gd32h75e_exmc.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_exmc.md",
    ".zed\\.projwiki\\modules\\gd32h75e_exti.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_exti.md",
    ".zed\\.projwiki\\modules\\gd32h75e_fac.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_fac.md",
    ".zed\\.projwiki\\modules\\gd32h75e_fmc.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_fmc.md",
    ".zed\\.projwiki\\modules\\gd32h75e_fwdgt.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_fwdgt.md",
    ".zed\\.projwiki\\modules\\gd32h75e_gpio.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_gpio.md",
    ".zed\\.projwiki\\modules\\gd32h75e_hpdf.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_hpdf.md",
    ".zed\\.projwiki\\modules\\gd32h75e_i2c.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_i2c.md",
    ".zed\\.projwiki\\modules\\gd32h75e_lpdts.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_lpdts.md",
    ".zed\\.projwiki\\modules\\gd32h75e_mdma.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_mdma.md",
    ".zed\\.projwiki\\modules\\gd32h75e_misc.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_misc.md",
    ".zed\\.projwiki\\modules\\gd32h75e_ospi.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_ospi.md",
    ".zed\\.projwiki\\modules\\gd32h75e_ospim.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_ospim.md",
    ".zed\\.projwiki\\modules\\gd32h75e_pmu.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_pmu.md",
    ".zed\\.projwiki\\modules\\gd32h75e_rameccmu.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_rameccmu.md",
    ".zed\\.projwiki\\modules\\gd32h75e_rcu.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_rcu.md",
    ".zed\\.projwiki\\modules\\gd32h75e_rtc.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_rtc.md",
    ".zed\\.projwiki\\modules\\gd32h75e_spi.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_spi.md",
    ".zed\\.projwiki\\modules\\gd32h75e_syscfg.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_syscfg.md",
    ".zed\\.projwiki\\modules\\gd32h75e_timer.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_timer.md",
    ".zed\\.projwiki\\modules\\gd32h75e_tmu.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_tmu.md",
    ".zed\\.projwiki\\modules\\gd32h75e_trigsel.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_trigsel.md",
    ".zed\\.projwiki\\modules\\gd32h75e_trng.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_trng.md",
    ".zed\\.projwiki\\modules\\gd32h75e_usart.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_usart.md",
    ".zed\\.projwiki\\modules\\gd32h75e_vref.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_vref.md",
    ".zed\\.projwiki\\modules\\gd32h75e_wwdgt.md": ".zed\\.projwiki\\modules\\bsp\\standard_peripheral\\gd32h75e_wwdgt.md",
}


def update_task_paths(task_file):
    """更新任务文件中的路径"""
    with open(task_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_count = 0
    for task in data.get("tasks", []):
        old_path = task.get("file_path", "")
        if old_path in PATH_MAPPING:
            task["file_path"] = PATH_MAPPING[old_path]
            updated_count += 1

    # 写回文件
    with open(task_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[OK] 更新了 {updated_count} 个任务的路径")
    return updated_count


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_task_paths.py <task_file.json>")
        sys.exit(1)

    task_file = sys.argv[1]
    update_task_paths(task_file)
