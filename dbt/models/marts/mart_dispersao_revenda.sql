with semanal as (
    select * from {{ ref('int_precos_municipio_semana') }}
)

select
    md5(concat_ws('|', uf, produto, cast(ano as varchar), cast(mes as varchar))) as id,
    uf,
    produto,
    ano,
    mes,
    count(distinct municipio) as qtd_municipios,
    sum(qtd_coletas) as qtd_coletas,
    min(preco_min_venda) as preco_min_venda,
    max(preco_max_venda) as preco_max_venda,
    max(preco_max_venda) - min(preco_min_venda) as amplitude_venda,
    round(stddev_samp(preco_medio_venda), 3) as desvio_padrao_municipal,
    round(
        100 * stddev_samp(preco_medio_venda)
        / nullif(avg(preco_medio_venda), 0), 2
    ) as coef_variacao_pct,
    avg(preco_medio_venda) - avg(preco_medio_compra) as margem_media
from semanal
group by uf, produto, ano, mes
