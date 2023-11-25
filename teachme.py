import random
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


crypto_origins = [
    "The origins of crypto are in cryptography, the practice of secure communication.",
    "Cryptocurrencies were envisioned as digital cash for direct transactions between parties.",
    "Bitcoin, created by Satoshi Nakamoto in 2009, was the first decentralized cryptocurrency.",
    "Satoshi Nakamoto's 2008 whitepaper, 'Bitcoin: A Peer-to-Peer Electronic Cash System', laid Bitcoin's foundation.",
    "Bitcoin's key innovation was blockchain technology for decentralization and solving double-spending.",
    "The first block in Bitcoin's blockchain, the genesis block, was mined by Nakamoto in January 2009.",
    "The first Bitcoin transaction was between Satoshi Nakamoto and Hal Finney in January 2009.",
    "Early Bitcoin adopters included enthusiasts, cypherpunks, and developers.",
    "Online forums, particularly BitcoinTalk, were pivotal in the early community and development of Bitcoin.",
    "The first real-world Bitcoin transaction was the purchase of two pizzas for 10,000 Bitcoins in 2010."
     "Ethereum's Introduction: Ethereum, proposed in late 2013 by Vitalik Buterin, is a major cryptocurrency that introduced the concept of a blockchain with a built-in programming language.",
    "Smart Contract Innovation: Ethereum's introduction of smart contracts enabled the creation of complex agreements, which execute automatically when conditions are met.",
    "The DAO Hack: In 2016, a decentralized autonomous organization (DAO) on Ethereum was hacked due to a smart contract vulnerability, leading to a significant split in the Ethereum network.",
    "Creation of Litecoin: Litecoin, created by Charlie Lee in 2011, was one of the first cryptocurrencies to follow Bitcoin and offered faster transaction confirmation times.",
    "Ripple and Real-Time Settlements: Ripple, introduced in 2012, focuses on enabling real-time cross-border payment systems.",
    "Bitcoin Halving: Bitcoin undergoes a halving event approximately every four years, which reduces the reward for mining new blocks by half, affecting the coin's inflation rate and scarcity.",
    "First ICO (Initial Coin Offering): Mastercoin conducted the first ICO in July 2013, introducing a new way of crowdfunding via cryptocurrency.",
    "Mt. Gox Hack: In 2014, Mt. Gox, one of the largest Bitcoin exchanges at the time, was hacked, leading to the loss of 850,000 Bitcoins.",
    "The Birth of Stablecoins: Tether, introduced in 2014, was one of the first stablecoins, cryptocurrencies designed to minimize volatility by pegging their market value to a currency or other external reference point.",
    "Cryptocurrency in Space: In 2016, Genesis Mining sent a Bitcoin paper wallet to space via a weather balloon at an altitude of 34 kilometers, symbolizing the borderless nature of cryptocurrencies.",
    "Introduction of Privacy Coins: Monero, launched in 2014, focuses on privacy and decentralization, using a special kind of cryptography to ensure that all transactions remain 100% unlinkable and untraceable.",
    "Bitcoin Cash Fork: In 2017, Bitcoin Cash was created as a result of a hard fork in the Bitcoin blockchain, primarily due to differences in scalability solutions.",
    "Surge of Decentralized Finance (DeFi): DeFi platforms began gaining significant traction around 2020, offering financial instruments without relying on intermediaries like banks.",
    "Non-Fungible Tokens (NFTs) Boom: 2021 saw a significant surge in the popularity of NFTs, with digital art and collectibles selling for millions of dollars.",
    "The Concept of Yield Farming: Yield farming became popular in the DeFi ecosystem, allowing cryptocurrency holders to lock up their holdings, which in turn provides them with rewards.",
    "Bitcoin's Legal Tender in El Salvador: In 2021, El Salvador became the first country to adopt Bitcoin as legal tender.",
    "The Rise of Decentralized Autonomous Organizations (DAOs): DAOs have gained prominence as a means of collective governance in the blockchain world.",
    "Ethereum 2.0 Transition: Ethereum has begun transitioning to Ethereum 2.0, shifting from proof-of-work to proof-of-stake to improve scalability and energy efficiency.",
    "Cryptocurrency and Environmental Concerns: The environmental impact of cryptocurrencies, particularly those that use proof-of-work, has been a topic of intense debate and scrutiny.",
    "The Role of Cryptocurrency in Global Finance: Cryptocurrencies are increasingly being viewed as potential tools for financial inclusion, offering services to those who are unbanked or underbanked."
    "The First Cryptocurrency Exchange: BitcoinMarket.com, launched in 2010, was the first-ever cryptocurrency exchange allowing Bitcoin trading for fiat currencies.",
    "Mt. Gox's Early Dominance: Established in 2010, Mt. Gox quickly became the largest Bitcoin exchange, handling over 70% of all Bitcoin transactions worldwide by 2013.",
    "Early Trading Pairs: Initially, most exchanges offered limited trading pairs, mainly focusing on Bitcoin-to-fiat currency trades.",
    "Regulatory Challenges: Early cryptocurrency exchanges faced significant regulatory uncertainties as governments worldwide began addressing digital currencies.",
    "Role in Price Discovery: Centralized exchanges were crucial in the price discovery of cryptocurrencies, especially when pricing data was scarce.",
    "Security Breaches: The early years of centralized exchanges were marred by security breaches, with the 2014 Mt. Gox hack being the most notable.",
    "Evolution of Exchange Features: Exchanges evolved from offering basic trading services to providing advanced features like margin trading, futures, and lending services.",
    "Emergence of KYC and AML Regulations: With increased regulatory scrutiny, exchanges began implementing Know Your Customer (KYC) and Anti-Money Laundering (AML) procedures.",
    "Expansion of Cryptocurrency Offerings: Centralized exchanges rapidly expanded their offerings to include a wide variety of altcoins and tokens as the market grew.",
    "Introduction of Stablecoins: The rise of stablecoins provided a significant boost to centralized exchanges, offering traders a way to hedge against volatility."
    "Dogecoin's Creation: Dogecoin was created in December 2013 as a 'joke currency', inspired by the 'Doge' meme.",
    "Shiba Inu (SHIB): Launched in 2020, SHIB is a Dogecoin spinoff, often referred to as the 'Dogecoin Killer'.",
    "Elon Musk's Influence: Tweets from Elon Musk have significantly influenced the price of Dogecoin.",
    "SafeMoon: Launched in 2021, SafeMoon includes a mechanism that rewards long-term holders.",
    "DogeDay: April 20 (4/20) has been unofficially branded as DogeDay by Dogecoin enthusiasts.",
    "Dogecoin's Market Cap: Dogecoin unexpectedly reached a market cap of over $70 billion in May 2021.",
    "Use Cases: Despite their origin, some meme coins like Dogecoin are used for tipping and donations online.",
    "Celebrity Endorsements: Dogecoin has been endorsed by celebrities like Snoop Dogg and Mark Cuban.",
    "Meme Coin Volatility: Meme coins are known for their extreme volatility and speculative nature.",
    "Akita Inu (AKITA): Another meme coin inspired by Shiba Inu, Akita Inu was launched in 2021.",
    "Kishu Inu: A meme coin that aims to be more than just a meme, with a wallet and NFT marketplace.",
    "Hoge Finance (HOGE): A deflationary meme coin where each transaction burns 2% of the value.",
    "The Dogecoin Foundation: Originally founded in 2014, it was revitalized in 2021 with a new advisory board.",
    "Elon Musk's 'Dogecoin to the Moon': Musk's SpaceX announced a lunar mission funded by Dogecoin.",
    "Baby Doge Coin: Launched in 2021, it gained popularity due to being a Dogecoin spinoff.",
    "MonaCoin (MONA): A Japanese meme coin featuring a cat-like character, created in 2013.",
    "PepeCash: A card-based meme coin linked to the Rare Pepe Directory of blockchain-certified Pepes.",
    "Nyancoin: Inspired by the 'Nyan Cat' meme, Nyancoin was introduced in 2014.",
    "Dogecoin's NASCAR Sponsorship: In 2014, the Dogecoin community sponsored a NASCAR driver.",
    "Banano (BAN): A meme coin that focuses on feeless transactions and a fun community."
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I am TeachMe Bot.")
    logging.info("Bot was started by a user.")

async def teachme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    fact = random.choice(crypto_origins)  # Changed from all_facts to crypto_origins
    formatted_message = f'*Crypto Fact:*\n{fact}'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=formatted_message, parse_mode='Markdown')
    logging.info(f"Sent a fact: {fact}")

def main() -> None:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    TOKEN = '6967926395:AAFQdOOtaxNUdHJx6LR0_WjunB64CZJINsI'  # Replace with your actual token
    application = Application.builder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    teachme_handler = CommandHandler('teachme', teachme)

    application.add_handler(start_handler)
    application.add_handler(teachme_handler)

    application.run_polling()

if __name__ == '__main__':
    main()