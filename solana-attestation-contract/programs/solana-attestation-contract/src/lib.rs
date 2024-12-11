use anchor_lang::prelude::*;

declare_id!("HCkvLKhWQ8TTRdoSry29epRZnAoEDhP9CjmDS8jLtY9");

const DISCRIMINATOR_SIZE: usize = 8;
const MAX_AUTHORITIES: usize = 10;

#[program]
pub mod solana_attestation_contract {

    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let authority_data = &mut ctx.accounts.authority_data;

        authority_data.admin = ctx.accounts.signer.key();

        Ok(())
    }

    pub fn add_proof(
        ctx: Context<AddProof>, 
        args: AddProofArgs
    ) -> Result<()> {
        let authority_data = &ctx.accounts.authority_data;

        let signer = ctx.accounts.authority.key();

        require!(authority_data.admin == signer || authority_data.authorities.contains(&signer), Errors::UnauthorizedSigner);

        let proof_record = &mut ctx.accounts.proof_record;

        proof_record.hashed_data = args.hashed_data;
        proof_record.signature = args.signature;
        proof_record.public_key = args.public_key;
        proof_record.attestation = args.attestation;

        Ok(())
    }

    pub fn add_authority(
        ctx: Context<AddAuthority>,
    ) -> Result<()> {
        let authority_data = &mut ctx.accounts.authority_data;
        let signer = ctx.accounts.signer.key();

        require!(authority_data.admin == signer, Errors::UnauthorizedSigner);
        require!(authority_data.authorities.len() < MAX_AUTHORITIES, Errors::MaxAuthoritiesReached);
        require!(!authority_data.authorities.contains(&ctx.accounts.new_authority.key()), Errors::AuthorityAlreadyExists);

        authority_data.authorities.push(ctx.accounts.new_authority.key());

        Ok(())
    }

    pub fn remove_authority(
        ctx: Context<RemoveAuthority>,
    ) -> Result<()> {
        let authority_data = &mut ctx.accounts.authority_data;
        let signer = ctx.accounts.signer.key();

        require!(authority_data.admin == signer, Errors::UnauthorizedSigner);
        require!(authority_data.authorities.contains(&ctx.accounts.authority.key()), Errors::AuthorityNotFound);

        // remove the authority from the vector
        authority_data.authorities.retain(|&x| x != ctx.accounts.authority.key());

        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init, 
        payer = signer, 
        space = DISCRIMINATOR_SIZE + AuthorityData::INIT_SPACE,
        seeds = [b"galadriel"],
        bump
    )]
    pub authority_data: Account<'info, AuthorityData>,

    #[account(mut)]
    pub signer: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct AddProofArgs {
    pub hashed_data: [u8; 32],
    pub signature: [u8; 64],
    pub public_key: [u8; 32],
    pub attestation: [u8; 32],
}

#[derive(Accounts)]
#[instruction(args: AddProofArgs)]
pub struct AddProof<'info> {
    #[account(
        init, 
        payer = authority, 
        space = DISCRIMINATOR_SIZE + ProofRecord::INIT_SPACE,
        seeds = [b"attestation", args.hashed_data.as_ref()],
        bump
    )]
    pub proof_record: Account<'info, ProofRecord>,

    #[account(
        seeds = [b"galadriel"],
        bump
    )]
    pub authority_data: Account<'info, AuthorityData>,
    
    #[account(mut)]
    pub authority: Signer<'info>,
    
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct AddAuthority<'info> {
    #[account(
        mut,
        seeds = [b"galadriel"],
        bump
    )]
    pub authority_data: Account<'info, AuthorityData>,

    #[account(mut)]
    pub signer: Signer<'info>,

    pub new_authority: SystemAccount<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct RemoveAuthority<'info> {
    #[account(
        mut,
        seeds = [b"galadriel"],
        bump
    )]
    pub authority_data: Account<'info, AuthorityData>,

    #[account(mut)]
    pub signer: Signer<'info>,

    pub authority: SystemAccount<'info>,

    pub system_program: Program<'info, System>,
}

#[account]
#[derive(InitSpace)]
pub struct AuthorityData {
    pub admin: Pubkey,
    #[max_len(MAX_AUTHORITIES)]
    pub authorities: Vec<Pubkey>
}

#[account]
#[derive(InitSpace)]
pub struct ProofRecord {
    pub hashed_data: [u8; 32],
    pub signature: [u8; 64],
    pub public_key: [u8; 32],
    pub attestation: [u8; 32],
}

#[error_code]
pub enum Errors {
    #[msg("Unauthorized signer")]
    UnauthorizedSigner,
    #[msg("Max authorities reached")]
    MaxAuthoritiesReached,
    #[msg("Authority already exists")]
    AuthorityAlreadyExists,
    #[msg("Authority not found")]
    AuthorityNotFound,
}
