use anchor_lang::prelude::*;

declare_id!("HCkvLKhWQ8TTRdoSry29epRZnAoEDhP9CjmDS8jLtY9");

const DISCRIMINATOR_SIZE: usize = 8;

#[program]
pub mod solana_attestation_contract {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {

        ctx.accounts.authority_data.authority = *ctx.accounts.authority.key;

        Ok(())
    }

    pub fn add_attestation(
        ctx: Context<AddAttestation>, 
        args: AddAttestationArgs
    ) -> Result<()> {
        let authority_data = &ctx.accounts.authority_data;

        require!(authority_data.authority == ctx.accounts.authority.key(), Errors::UnauthorizedSigner);

        let attestation_record = &mut ctx.accounts.attestation_record;

        attestation_record.hashed_data = args.hashed_data;
        attestation_record.signature = args.signature;
        attestation_record.public_key = args.public_key;
        attestation_record.attestation = args.attestation;

        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init, 
        payer = authority, 
        space = DISCRIMINATOR_SIZE + AuthorityData::INIT_SPACE,
        seeds = [b"galadriel"],
        bump
    )]
    pub authority_data: Account<'info, AuthorityData>,

    #[account(mut)]
    pub authority: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct AddAttestationArgs {
    pub hashed_data: [u8; 32],
    pub signature: [u8; 64],
    pub public_key: [u8; 32],
    pub attestation: [u8; 32],
}

#[derive(Accounts)]
#[instruction(args: AddAttestationArgs)]
pub struct AddAttestation<'info> {
    #[account(
        init, 
        payer = authority, 
        space = DISCRIMINATOR_SIZE + AttestationRecord::INIT_SPACE,
        seeds = [b"attestation", args.hashed_data.as_ref()],
        bump
    )]
    pub attestation_record: Account<'info, AttestationRecord>,

    #[account(
        seeds = [b"galadriel"],
        bump
    )]
    pub authority_data: Account<'info, AuthorityData>,
    
    #[account(mut)]
    pub authority: Signer<'info>,
    
    pub system_program: Program<'info, System>,
}

#[account]
#[derive(InitSpace)]
pub struct AuthorityData {
    pub authority: Pubkey
}

#[account]
#[derive(InitSpace)]
pub struct AttestationRecord {
    pub hashed_data: [u8; 32],
    pub signature: [u8; 64],
    pub public_key: [u8; 32],
    pub attestation: [u8; 32],
}

#[error_code]
pub enum Errors {
    #[msg("Unauthorized signer")]
    UnauthorizedSigner,
}
