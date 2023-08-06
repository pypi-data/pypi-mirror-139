from random import Random
from wai.common.cli.options import TypedOption, FlagOption
from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image import ImageInstance

MIN_RAND = 0
MAX_RAND = 1000


class BaseISP(
    RequiresNoFinalisation,
    ProcessorComponent[ImageInstance, ImageInstance]
):
    """
    Base class for stream processors that augment images.
    """

    seed = TypedOption(
        "-s", "--seed",
        type=int,
        help="the seed value to use for the random number generator; randomly seeded if not provided"
    )

    seed_augmentation = FlagOption(
        "-a", "--seed-augmentation",
        help="whether to seed the augmentation; if specified, uses the seeded random generator to produce a seed value from %d to %d for the augmentation." % (MIN_RAND, MAX_RAND)
    )

    threshold = TypedOption(
        "-T", "--threshold",
        type=float,
        help="the threshold to use for Random.rand(): if equal or above, augmentation gets applied; range: 0-1; default: 0 (= always)"
    )

    def _can_augment(self):
        """
        Checks whether augmentation can take place.

        :return: whether can augment
        :rtype: bool
        """
        return True

    def _augment(self, element: ImageInstance, aug_seed: int):
        """
        Augments the image.

        :param element: the image to augment
        :type element: ImageInstance
        :param aug_seed: the seed value to use, can be None
        :type aug_seed: int
        :return: the potentially updated image
        :rtype: ImageInstance
        """
        raise NotImplementedError()

    def process_element(
            self,
            element: ImageInstance,
            then: ThenFunction[ImageInstance],
            done: DoneFunction
    ):
        # can we augment?
        if not self._can_augment():
            then(element)
            return

        threshold = 0.0 if self.threshold is None else self.threshold
        if (threshold < 0) or (threshold > 1):
            raise Exception("Threshold must satisfy x >= 0 and x <= 1, supplied: %f" % threshold)

        if not hasattr(self, "_random"):
            self._random = Random(self.seed)

        if self._random.random() < threshold:
            then(element)
            return

        # augment
        if self.seed_augmentation:
            aug_seed = self._random.randint(MIN_RAND, MAX_RAND)
        else:
            aug_seed = None
        element_out = self._augment(element, aug_seed)

        then(element_out)
