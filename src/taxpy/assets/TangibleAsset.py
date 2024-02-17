"""
tangible_assets.py
"""

from src.taxpy.assets.Asset import Asset


class TangibleAsset(Asset):
    def __init__(self, name: str, life: int, value: float, slvg_value: float = 0.0, prod_cap: int = 0) -> None:
        """
        :param name: The name of the asset.
        :param life: The life of the asset (months).
        :param value: The value of the asset ($).
        :param slvg_value: The salvage value of the asset, if any ($).
        :param prod_cap: The production capacity of the asset (if applicable).
        """
        super().__init__(name, life, value)
        self.SLVG_VALUE: float = slvg_value
        self.prod_cap: int = prod_cap

        # This is the $ amount that can be depreciated.
        self.depreciable_value: float = self.value - self.SLVG_VALUE
        self.last_depr: float = 0.0
        self.total_depr: float = 0.0

    def reset(self) -> None:
        super().reset()
        self.depreciable_value = self.value - self.SLVG_VALUE
        self.last_depr = 0.0
        self.total_depr = 0.0

    def change_value(self, new_value: float) -> None:
        super().change_value(new_value)
        self.depreciable_value = self.value - self.SLVG_VALUE

    def _update_attribs(self, periods: int) -> None:
        """
        Re-runs all values to make sure they're consistent with each other. Used after depreciating.
        :param periods:
        :return: Nothing.
        """
        self.value -= self.last_depr
        self.depreciable_value = self.value - self.SLVG_VALUE
        self.rem_life -= periods
        self.total_depr += self.last_depr

    def depreciate(self, method: int, periods: int = 1, decline: float = 1.0, units_prod: int = 0) -> float:
        """
        [Supported Depreciation Methods] \n
        0: Straight Line Method \n
        1: Declining Balance Method \n
        2: Sum of the Years' Digits Method \n
        3: Units of Production Method \n
        :param method: The depreciation method.
        :param periods: The number of periods (months) to depreciate.
        :param decline: The factor used in the declining balance method (2.0 = 200%).
        :param units_prod: How many units produced, if using method 3.
        :return: The dollar value depreciated.
        """
        # The only time I can foresee this conditional being necessary is for the declining balance method,
        # since it ignores salvage value in its calculation of depreciation while not depreciating below salvage value.
        if self.depreciable_value > 0:
            match method:
                # Straight Line
                case 0:
                    self.last_depr = ((self.DEF_VALUE - self.SLVG_VALUE) / self.LIFE) * periods
                    self._update_attribs(periods)

                # Declining Balance
                case 1:
                    self.last_depr = (((self.DEF_VALUE - self.total_depr) / self.LIFE) * decline) * periods
                    self._update_attribs(periods)

                # Sum of the Years' Digits
                case 2:
                    self.last_depr = self.DEF_VALUE * (self.rem_life / self.syd)
                    self._update_attribs(periods)

                # Units of Production
                case 3:
                    self.last_depr = (self.depreciable_value / self.prod_cap) * units_prod
                    self._update_attribs(periods)

        else:
            if self.depreciable_value < 0:
                self.depreciable_value = 0

            print(f"Asset \"{self.name}\" is fully depreciated! Current value = {self.value}.")
            self.last_depr = 0.0

        return self.last_depr
