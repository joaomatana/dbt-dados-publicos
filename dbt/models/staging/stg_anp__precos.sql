with origem as (
    select * from {{ source('anp', 'precos') }}
)

select
    nullif(trim(regexp_replace("Regiao - Sigla", '[\r\n]', '', 'g')), '') as regiao,
    upper(nullif(trim(regexp_replace("Estado - Sigla", '[\r\n]', '', 'g')), '')) as uf,
    nullif(trim("Municipio"), '') as municipio,
    nullif(trim("Revenda"), '') as revenda,
    nullif(trim("CNPJ da Revenda"), '') as cnpj_revenda,
    nullif(trim("Bandeira"), '') as bandeira,
    nullif(trim("Produto"), '') as produto,
    try_strptime(trim("Data da Coleta"), '%d/%m/%Y')::date as data_coleta,
    try_cast(replace(nullif(trim("Valor de Venda"), ''), ',', '.') as decimal(10, 3)) as valor_venda,
    try_cast(replace(nullif(trim("Valor de Compra"), ''), ',', '.') as decimal(10, 3)) as valor_compra,
    nullif(trim("Unidade de Medida"), '') as unidade_medida,
    _arquivo_origem,
    _loaded_at
from origem
where nullif(trim("Produto"), '') is not null
