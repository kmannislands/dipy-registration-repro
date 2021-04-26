from dipy.align.imaffine import (
    MutualInformationMetric,
    AffineRegistration,
)

def get_affine_registration(level_iters) -> AffineRegistration:
    """
    """
    # The number of bins used determines how sensitive the measurement of entropy is to variance in the voxel intensity
    # A small number of bins decreases sensitivity
    n_bins = 128

    # No sampling prop is used
    sampling_prop = None
    metric = MutualInformationMetric(n_bins, sampling_prop)

    sigmas = [3.0, 1.0, 0.0]
    factors = [4, 2, 1]

    aff_reg = AffineRegistration(
        metric=metric, level_iters=level_iters, sigmas=sigmas, factors=factors
    )

    return aff_reg

def apply_transform(
    transform,
    template_data,
    moving_data,
    template_affine,
    moving_affine,
    affine_map,
    aff_reg,
):
    params0 = None
    starting_affine = affine_map.affine

    affine_transform = aff_reg.optimize(
        template_data,
        moving_data,
        transform,
        params0,
        template_affine,
        moving_affine,
        starting_affine,
    )

    transformed_moving_data = affine_transform.transform(moving_data)

    return transformed_moving_data, affine_transform