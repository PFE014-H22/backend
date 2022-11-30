
import unittest

from src.config_parameters.technologies import find_parameter


class TestFindParameters(unittest.TestCase):

    CASSANDRA_PARAMETER_FILE = "./src/config_parameters/cassandra/cassandra_parameters.txt"

    text = """
    cluster_name Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi in felis turpis. Suspendisse hendrerit imperdiet consectetur. Quisque mi turpis, rutrum malesuada purus posuere, mattis imperdiet dui. Praesent dignissim ante nibh, a eleifend sem efficitur ac. Mauris sollicitudin, nulla sed pulvinar rhoncus, arcu ipsum eleifend odio, vel pretium erat felis ac ex. Integer nisi quam, finibus ac erat nec, congue mattis justo. Aenean eget cursus nibh. Nulla maximus mauris sit amet nunc tristique, euismod aliquam leo interdum. Aliquam egestas auctor nisl. Sed porttitor urna sit amet tortor luctus placerat.

    Cras quis aliquet justo, vel auctor ex. Donec tincidunt felis turpis, nec tincidunt nunc auctor eget. Sed tincidunt malesuada dolor, nec posuere lectus. Etiam egestas scelerisque enim, ac tincidunt tellus dictum id. Sed a elementum mauris. Nulla pretium sapien eu tempus volutpat. Donec fermentum in dui aliquet hendrerit. Fusce placerat, libero ut commodo ultrices, mi leo molestie arcu, sed convallis lorem purus a massa. Sed aliquam sapien turpis, at aliquam mi facilisis a. Sed tincidunt, lorem sed ullamcorper euismod, leo metus laoreet erat, ac sodales augue metus vel erat. Ut quis massa eu tellus sagittis aliquet ut a nulla. Morbi dictum, justo ac pellentesque porttitor, eros leo consequat tortor, ut ultrices elit mauris sed massa. Duis nec massa vel nulla vestibulum tincidunt.

    Aliquam ut ex lectus. Phasellus scelerisque elementum rhoncus. Suspendisse potenti. Duis finibus finibus ultricies. Morbi nec sagittis purus. Ut aliquet sodales leo vitae ornare. Nam vulputate pharetra dui, id faucibus mi efficitur ut. Vestibulum ac lectus in massa euismod vehicula malesuada in erat. In finibus orci quis dui consequat pellentesque. Nulla ipsum est, dignissim sed hendrerit sed, convallis sed nisl. Quisque a tristique turpis. Phasellus scelerisque eros sit amet ipsum sollicitudin lobortis. Integer dictum ligula at dapibus egestas. Integer eu nibh quis lectus cursus semper. Nunc volutpat dui quis metus cursus, et sodales lectus cursus.

    Aliquam aliquet aliquam justo, eget vehicula libero aliquet vitae. Curabitur max_hints_delivery_threads imperdiet odio id est condimentum, in auctor tortor porttitor. Suspendisse nisi ligula, tristique cursus porttitor et, efficitur et nisi. Maecenas efficitur scelerisque arcu, ut convallis orci rhoncus a. Proin elit elit, efficitur aliquet consectetur et, lacinia nec metus. Aliquam erat volutpat. In est eros, ornare vitae elit non, ornare elementum magna. Vestibulum convallis bibendum sem, non ornare arcu dictum facilisis. Vivamus eget malesuada quam.

    Vestibulum tincidunt neque a massa fringilla condimentum. Donec ac ultricies erat. Sed commodo et nunc nec placerat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas quis lectus eu elit imperdiet prefer_local tempor a eu justo. Aliquam rhoncus lobortis metus, at iaculis nulla auctor eu. Nulla eleifend blandit nulla. Duis vitae sem eu diam feugiat molestie. Proin porttitor auctor rhoncus. Nam tempor volutpat dapibus. Sed diam nulla, tincidunt a pharetra iaculis, malesuada ac orci. Nam sollicitudin justo vel pulvinar condimentum. Nunc congue quam a est vehicula, in dignissim libero consectetur
    """

    def test_findParameters(self):
        expected_parameter = [
            'prefer_local',
            'cluster_name',
            'max_hints_delivery_threads',
        ]

        parameters_found = find_parameter(
            text=self.text,
            parameter_file=self.CASSANDRA_PARAMETER_FILE
        )

        self.assertEqual(
            sorted(expected_parameter),
            sorted(parameters_found)
        )


if __name__ == '__main__':
    unittest.main()
