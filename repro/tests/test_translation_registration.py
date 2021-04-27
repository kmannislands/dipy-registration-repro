import pickle
import logging
from pathlib import Path

import numpy as np

from dipy.align.transforms import (
    TranslationTransform3D,
    RigidTransform3D,
)

from repro.helpers import (
    apply_transform,
    get_affine_registration
)

TEST_RESOURCE_PATH =  Path(__file__).parent / Path('../test_resources')

AFFINE_MAP_SNAPSHOT_PATH_INPUT = TEST_RESOURCE_PATH / "new_input_snap.pkl"
AFFINE_MAP_TRANSLATION_SNAPSHOT_PATH_OUTPUT = TEST_RESOURCE_PATH / "new_output_snap.pkl"
AFFINE_MAP_RIGID_SNAPSHOT_PATH_OUTPUT = TEST_RESOURCE_PATH / "new_output_rigid_snap.pkl"

logger = logging.getLogger(__name__)

def test_affine_map_translation_snapshot():
    assert AFFINE_MAP_SNAPSHOT_PATH_INPUT.exists()
    assert AFFINE_MAP_TRANSLATION_SNAPSHOT_PATH_OUTPUT.exists()

    """
        Loads a pickled data object with all the inputs and outputs for a call to apply_transform

        transformed, curr_affine = apply_transform(
            TranslationTransform3D(),
            template_data,
            moving_data,
            template_affine,
            moving_affine,
            curr_affine,
            affreg,
            plot,
        )
    """
    with open(AFFINE_MAP_SNAPSHOT_PATH_INPUT, "rb") as input_file:
        input_snapshot = pickle.load(input_file)

    with open(AFFINE_MAP_TRANSLATION_SNAPSHOT_PATH_OUTPUT, "rb") as input_file:
        output_snapshot = pickle.load(input_file)

    aff_reg = get_affine_registration([100, 20, 10])

    transformed, curr_affine = apply_transform(
        TranslationTransform3D(),
        input_snapshot["template_data"],
        input_snapshot["moving_data"],
        input_snapshot["template_affine"],
        input_snapshot["moving_affine"],
        input_snapshot["curr_affine"],
        aff_reg,
    )

    logger.info(f"Output registration affine: {curr_affine}")

    logger.info(f"Target registration affine: {output_snapshot['curr_affine']}")

    assert np.all(
        np.equal(curr_affine.affine, output_snapshot["curr_affine"].affine)
    ), "Expected registration affine to match target registration affine generated on macOs"

    assert np.all(
        np.equal(transformed, output_snapshot["transformed"])
    ), "Expected transformed image to match target transformed image generated on macOs"

def test_affine_map_rigid_snapshot():
    assert AFFINE_MAP_SNAPSHOT_PATH_INPUT.exists()
    assert AFFINE_MAP_RIGID_SNAPSHOT_PATH_OUTPUT.exists()

    with open(AFFINE_MAP_SNAPSHOT_PATH_INPUT, "rb") as input_file:
        input_snapshot = pickle.load(input_file)

    with open(AFFINE_MAP_RIGID_SNAPSHOT_PATH_OUTPUT, "rb") as input_file:
        output_snapshot = pickle.load(input_file)

    aff_reg = get_affine_registration([100, 20, 10])

    transformed, curr_affine = apply_transform(
        RigidTransform3D(),
        input_snapshot["template_data"],
        input_snapshot["moving_data"],
        input_snapshot["template_affine"],
        input_snapshot["moving_affine"],
        input_snapshot["curr_affine"],
        aff_reg,
    )

    # TODO remove this, this is how "snapshot" pickles were produced:
    # with open(AFFINE_MAP_RIGID_SNAPSHOT_PATH_OUTPUT, 'wb') as snap_out:
    #     outputs = {
    #         'transformed': transformed,
    #         'affine': curr_affine
    #     }
    #     pickle.dump(outputs, snap_out)

    logger.info(f"Output registration affine: {curr_affine}")

    logger.info(f"Target registration affine: {output_snapshot['affine']}")

    assert np.all(
        np.equal(curr_affine.affine, output_snapshot["affine"].affine)
    ), "Expected registration affine to match target registration affine generated on macOs"

    assert np.all(
        np.equal(transformed, output_snapshot["transformed"])
    ), "Expected transformed image to match target transformed image generated on macOs"
