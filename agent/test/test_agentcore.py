import boto3
import json

client = boto3.client('bedrock-agentcore', region_name='us-west-2')
payload = json.dumps(
    # {
    #     "user_message": "万年青",
    #     "image_url": "https://storage.googleapis.com/flower-db-prd/075718a0ef158669af0625026c34a321.jpg"
    # }
    # {
    #     "user_message": "植物",
    #     "image_url": "https://ai-gpt-eval-images.s3.us-west-2.amazonaws.com/a1.JPG?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBoaCXVzLXdlc3QtMiJGMEQCIBAVs1gn8h2dee4UmUJdpvaKj7SYP8DRPNaqk41yfqmPAiBOgNYCPvdS0%2BY4Gi6A3NMr2julYoe4k0AlmhhVLHo7oCrQBAjj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDE5NzU3ODAzNzI4NiIM%2BDiRXDgceikE3WPEKqQE39AwWaQvLdgQDYzGEap%2FOq62F0VdXdm98EVpQFXfmlXW4KOL6niIFgZwVDbgIz8tuyO5qIqdtqj3wbwxqQGr1LFLGzKh7E5GpTYcVbUoelCA12jzK9TvkjE1YT0cMXXJe9HVE8Rt%2Fck%2F4RkQEXLasfiL1cT37%2BH1OTDRn5YSI%2BaXkQcfs89%2FDYcc%2FNjj4tVQkGcEv7MKElzWYHwmh2saIMKb7pd8x%2BpDZ8sbH82FDIpcEDqAbmTrroY0ceLQNm1LftH2H9NdlD0NT%2BVDEBzl4ZAvSAmaO15lEiGKyjGngZXmFmwc1UDX6DMO6QolpG1gwg18HbnJBegJ0xwbR5MqXo%2B%2Fuo7WSWKwCb9t%2BbBidHE7c9kuJJMagfo%2F5ICvhpTok4Y7DMDXx1ksKJdSB3WSvAOujHegT7mKDFxsB%2Bm13bWjFrzPO40R%2FQ4If8svMum0TXaQdlfeXoVk8gm0KTzRbk%2FzRmRC6K%2BAJ79BntbGe3QCUa3xDeWSfdbNlWzCA8b6lzuJDzi8XCd1G%2FmcIjtiZCmstoMKwj7nzA1TRuteSQ3akyREiBsBqJC3FSYaOmMdyyQjBUx2k3Qz5ImkGiLw3iHtohE7zkr9dEKpIQd11vLWgna5PXlzoS6tTRojMZ6BZnOdNAr8b2kvGW7xAn2Wf0WGJDFgVjOBDFlEIIHrabDW7ADFSaM4S63hIOc%2FXQypZJ8P4U7sAxqDvjIb%2B1FHXtu7At4w3%2BCBzAY6xAJZ0oGjz3R6VaHkT%2BY2nU1bGgoZGMkHCgOW%2BXlzc6fHd2ga3RmwfuepheEUHyWmuAx3Jli6i9pfY3Z1EgHUFlkeBHmZRGh%2FUq9WSJRzXK8JmaH1ScyiBHxQ1DthZ4Cjea2GYYAplwHTUvrSltPbLz9is1uf2vuGd7zUjjfzfsBD22TzReLLDZ%2FhsFCsJ52xaMbJ8CaWu8YGM7FoobyvTI8WlBytViASPbDSadgPRxoALhluG4DF92V2UP8J9kFRP9m6CcmPBhot8lbxjCVhTBjKj3xoUhileICt94ShDbLc2jC0ye9dgyaeJSLcjvPYmSex6Z61YmDB6iOACRbur43t6cXK8%2BmxpgPjqf6fheeHq5GbhD4weslqc8l2J7MouqZQeMPZsA5mIIMrhUkoaEx6mMETe57Yf%2Bz82judKPTSQnUVJ8c%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAS4AERTATAXKNPUN6%2F20260202%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260202T093910Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=bb348889c794b3cddc3fe2de31f2efdc3bcbc7431b06dd5cefa2f2dc18e36473"
    # }
    {
        "user_message": "长日照植物"
        # "image_url": "https://ai-gpt-eval-images.s3.us-west-2.amazonaws.com/a1.JPG?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjECoaCXVzLXdlc3QtMiJGMEQCIEU4%2FexUwv0FaTxR0GObaTXd5Sddxa74CWctey7wb0cyAiBHw4r9maY2Knt0HhiMpGNyQTL1nC5xV6JSswpW%2FsxP6CrQBAjz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDE5NzU3ODAzNzI4NiIMlmESeX6VdA9pDvqAKqQEcbzpw2CmxiYSclAGA1TMbu4ualsdTirHOFi2blzaqYJUPhSLn%2B7J%2FCAv4RT%2FCZLJubF9zxWdzpA128EbM8vhTcnrVu9D%2BZx7WcN6UJuSG7UnvLa6fXmamAmLXl6aXv4kkhR0JInRwWLMmv5jQAgI5LFE8DGGSO4qBq4hCoMGXXwFW552yD2lwcPhtVX9Tgzfy%2FIJ4tJ%2FXddkoYe%2FbrZcxPz4HF2nsldoaKf6suVog%2FSfdgTJr3TE2xGWmnEqZhXxZhCqBohsxmvGoe2XJvks43ZFMaUJ7C5bQLM8Q8R%2F5mJvRMXC8Qc%2Fm%2Fe9mEZIO23QxsSbMPgGxRZjdsWf%2B4ywkthXuUbGmpjpxDmqxgOmmkKmoiHooOZ7CtI%2Bdju3BEa2tKHXn6zLkhAcbr%2BIi4JerefQGB27ReGGFDGgzjc9oIcQjI6qwhqqgWnkkXJYdpSgcs6vlfXTs9x5y2goOSQtb4RT8RF0J757hjEb%2FWNHNpf2fgD8CWvtNBEIqdYFp5IOBvN8dH3FkYDG7u8bKPeRC28jdFx2Z1GNV7jcwWJ%2Bn1TDPL7iBkFxKese2VHgWXUFjhCeA138TKv3sdfEiABVOi8lKSssNT%2FqgX8gs8fQTUDbtj%2BSH3JmpP3CcmaRt%2FIfWEs0xFwy87GeWjSnT6vGv8ldI2h3YplfNb5fs0ZR6f6UWjyVhSLCF69WHbIKKddEN%2BUc5he8elq%2BaBO4NAIWiUzLkRsw4LCFzAY6xAJPiJU0lSvus8aOorfB13SnGGGmhRQFsBUxg%2FbblxeYiOd4DhwKTuiTOGNbMEiORZtBt5UjjuNKMRMHIxOKi2kbjR6WS7YiBElBErWcoaKH6CRyDvoh0RwhDWvYcGvfGclFqRBIXhmm7geyCw8Wsq8bJftl8oXAYZACWJB3UdzgDqCNESSQQlXxIBa1exADyUvCdcPdXXeCreXBo4G%2BcZwB4LymWLEoE%2BkGO%2BeKjNXip4liP4WhhacsV47n7POU%2Fxa0EuBjxIH%2F8czLaFum%2B6vom6HzomzPPiXiRBMuuV1yfNtYQ5Le8sj7GYvCxT8rB3RRK2y3Bp%2BIkM5f%2BMVd%2Bc9RgfRG2UbY8xtCO2ngHRpPXvrlj81TFUM7ZC98PAxoTSeeOsZJuai2Rzud4qp3z3tHGgmlfLjd6MFRhBHjcEYJBTefpCQ%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAS4AERTATJDXVHAJL%2F20260203%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260203T020942Z&X-Amz-Expires=28800&X-Amz-SignedHeaders=host&X-Amz-Signature=adfaa79b0e7c3aa3fd02d02c35f3e1e41cb39bc58dc8c892f8de199267b99684"
    }
)
response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-west-2:533267235251:runtime/grow_light-2VJhSK5zPc',
    runtimeSessionId='e37d91c1-8d94-4099-9542-fe249bc7e642', # Must be 33+ char. Every new SessionId will create a new MicroVM
    payload=payload,
)
response_body = response['response'].read()
response_data = json.loads(response_body)
print(response_data)