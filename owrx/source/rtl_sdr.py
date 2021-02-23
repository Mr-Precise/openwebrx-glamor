from owrx.source.connector import ConnectorSource, ConnectorDeviceDescription
from owrx.command import Flag, Option
from typing import List
from owrx.form import Input, TextInput
from owrx.form.device import BiasTeeInput, DirectSamplingInput


class RtlSdrSource(ConnectorSource):
    def getCommandMapper(self):
        return (
            super()
            .getCommandMapper()
            .setBase("rtl_connector")
            .setMappings({"bias_tee": Flag("-b"), "direct_sampling": Option("-e")})
        )


class RtlSdrDeviceDescription(ConnectorDeviceDescription):
    def getInputs(self) -> List[Input]:
        return super().getInputs() + [
            TextInput(
                "device",
                "Device identifier",
                infotext="Device serial number or index",
            ),
            BiasTeeInput(),
            DirectSamplingInput(),
        ]

    def getOptionalKeys(self):
        return super().getOptionalKeys() + ["device", "bias_tee", "direct_sampling"]

    def getProfileOptionalKeys(self):
        return super().getProfileOptionalKeys() + ["bias_tee", "direct_sampling"]
