'''
# CDK Triggers

## This project has graduated from incubation and is now part of the AWS CDK. It is no longer maintained in this repository

Please refer to the official AWS CDK documentation:

* [Documentation](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.triggers-readme.html)
* [Source Code](https://github.com/aws/aws-cdk/tree/master/packages/%40aws-cdk/triggers)

## Usage

```python
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as triggers from 'aws-cdk-lib/triggers';
import { Stack } from 'aws-cdk-lib';
import { Construct } from 'constructs';

declare const stack: Stack;
declare const resource1: Construct;
declare const resource2: Construct;

new triggers.TriggerFunction(stack, 'MyTrigger', {
  runtime: lambda.Runtime.NODEJS_12_X,
  handler: 'index.handler',
  code: lambda.Code.fromAsset(__dirname + '/my-trigger'),
  executeAfter: [resource1, resource2],
});
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_lambda
import constructs


class AfterCreate(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-triggers.AfterCreate",
):
    '''
    :stability: deprecated
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        handler: aws_cdk.aws_lambda.Function,
        resources: typing.Optional[typing.Sequence[constructs.Construct]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param handler: (deprecated) The handler to execute once after all the resources are created. The trigger will be executed every time the handler changes (code or configuration).
        :param resources: (deprecated) Resources to trigger on. Resources can come from any stack in the app. Default: [] Run the trigger at any time during stack deployment.

        :stability: deprecated
        '''
        props = AfterCreateProps(handler=handler, resources=resources)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-triggers.AfterCreateProps",
    jsii_struct_bases=[],
    name_mapping={"handler": "handler", "resources": "resources"},
)
class AfterCreateProps:
    def __init__(
        self,
        *,
        handler: aws_cdk.aws_lambda.Function,
        resources: typing.Optional[typing.Sequence[constructs.Construct]] = None,
    ) -> None:
        '''
        :param handler: (deprecated) The handler to execute once after all the resources are created. The trigger will be executed every time the handler changes (code or configuration).
        :param resources: (deprecated) Resources to trigger on. Resources can come from any stack in the app. Default: [] Run the trigger at any time during stack deployment.

        :stability: deprecated
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "handler": handler,
        }
        if resources is not None:
            self._values["resources"] = resources

    @builtins.property
    def handler(self) -> aws_cdk.aws_lambda.Function:
        '''(deprecated) The handler to execute once after all the resources are created.

        The trigger will be executed every time the handler changes (code or
        configuration).

        :stability: deprecated
        '''
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(aws_cdk.aws_lambda.Function, result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[constructs.Construct]]:
        '''(deprecated) Resources to trigger on.

        Resources can come from any stack in the app.

        :default: [] Run the trigger at any time during stack deployment.

        :stability: deprecated
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[constructs.Construct]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AfterCreateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AfterCreate",
    "AfterCreateProps",
]

publication.publish()
