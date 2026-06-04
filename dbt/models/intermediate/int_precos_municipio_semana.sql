with precos as (
    select *
    from {{ ref('stg_anp__precos') }}
    where data_coleta is not null and valor_venda is not null
)

select
    md5(concat_ws(
        '|', uf, municipio, produto,
        cast(ano as varchar), cast(mes as varchar),
        cast(num_semana as varchar)
    )) as id,
    regiao,
    uf,
    municipio,
    produto,
    ano,
    mes,
    num_semana,
    inicio_semana,
    count(*) as qtd_coletas,
    sum(valor_venda) as soma_valor_venda,
    avg(valor_venda) as preco_medio_venda,
    min(valor_venda) as preco_min_venda,
    max(valor_venda) as preco_max_venda,
    avg(valor_compra) as preco_medio_compra
from (
    select
        *,
        year(data_coleta) as ano,
        month(data_coleta) as mes,
        week(data_coleta) as num_semana,
        date_trunc('week', data_coleta) as inicio_semana
    from precos
)
group by regiao, uf, municipio, produto, ano, mes, num_semana, inicio_semana
