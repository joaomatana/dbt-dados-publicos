with semanal as (
    select * from {{ ref('int_precos_municipio_semana') }}
)

select
    md5(concat_ws('|', uf, produto, cast(ano as varchar), cast(mes as varchar))) as id,
    uf,
    produto,
    ano,
    mes,
    sum(soma_valor_venda) / nullif(sum(qtd_coletas), 0) as preco_medio_venda,
    min(preco_min_venda) as preco_min_venda,
    max(preco_max_venda) as preco_max_venda,
    sum(qtd_coletas) as qtd_coletas,
    count(distinct municipio) as qtd_municipios
from semanal
group by uf, produto, ano, mes
