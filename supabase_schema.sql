-- Run this script once in Supabase Dashboard > SQL Editor.
-- The application uses the server-only SUPABASE_SECRET_KEY on Render.

create table if not exists public.clients (
    client_id text primary key,
    full_name text not null,
    matter text not null,
    total_amount bigint not null,
    pays_in_installments text not null,
    installment_count integer not null default 0,
    first_installment_date date,
    created_at date not null,
    status text not null default 'active'
);

create table if not exists public.installments (
    installment_id text primary key,
    client_id text not null,
    number integer not null,
    kind text not null,
    scheduled_amount bigint not null,
    due_date date not null,
    reference_month text not null
);

create table if not exists public.payments (
    payment_id text primary key,
    client_id text not null,
    installment_id text not null,
    payment_date date not null,
    amount bigint not null,
    receipt_issued text not null,
    note text not null default ''
);

create index if not exists installments_client_id_idx on public.installments (client_id);
create index if not exists payments_client_id_idx on public.payments (client_id);
create index if not exists payments_installment_id_idx on public.payments (installment_id);
