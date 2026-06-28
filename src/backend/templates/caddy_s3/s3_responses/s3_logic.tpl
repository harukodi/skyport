{{- .RespHeader.Set "x-amz-request-id" (randAlphaNum 16 | upper) -}}
{{- .RespHeader.Set "x-amz-id-2" (printf "%s-%s" .Host (env "HOSTNAME") | sha256sum) -}}