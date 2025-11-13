from datetime import datetime

from hamcrest import (
    assert_that,
    starts_with,
    all_of,
    has_property,
    instance_of,
    has_properties,
    equal_to,
)


class GetV1Account:
    @classmethod
    def check_response_values(
            cls,
            response
    ):
        assert_that(
            response, all_of(
                has_property('resource', has_property('login', starts_with('kirka'))),
                has_property('resource', has_property('registration', instance_of(datetime))),
                has_property(
                    'resource', has_properties(
                        {
                            'rating': has_properties(
                                {
                                    "enabled": equal_to(True),
                                    "quality": equal_to(0),
                                    "quantity": equal_to(0)
                                }
                            )
                        }
                    )
                )
            )
        )
